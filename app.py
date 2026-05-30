from flask import Flask, render_template, request, jsonify
import yfinance as yf
import anthropic
import os
import re
import json
import time
import requests
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

try:
    from yfinance.exceptions import YFRateLimitError
except ImportError:
    class YFRateLimitError(Exception):
        pass

load_dotenv()
app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'history.db')

YF_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

# ===== TW COMPANY NAME LOOKUP =====

_TW_COMPANY_CACHE = {}  # ticker_num -> {'name': '公司名稱', 'short': '公司簡稱'}

def _load_tw_company_list():
    """Load TWSE + TPEX company list once and cache."""
    if _TW_COMPANY_CACHE:
        return
    sources = [
        'https://openapi.twse.com.tw/v1/opendata/t187ap03_L',   # TWSE listed
        'https://openapi.twse.com.tw/v1/opendata/t187ap03_R',   # TPEX OTC
    ]
    for url in sources:
        try:
            r = requests.get(url, timeout=10)
            for item in r.json():
                code = str(item.get('公司代號', '')).strip()
                if code:
                    _TW_COMPANY_CACHE[code] = {
                        'name': item.get('公司名稱', ''),
                        'short': item.get('公司簡稱', ''),
                    }
        except Exception:
            pass

def get_tw_company_name(ticker_num: str) -> str:
    """Return Chinese company name for a TW ticker number, or empty string."""
    _load_tw_company_list()
    entry = _TW_COMPANY_CACHE.get(ticker_num.upper().replace('.TW', '').replace('.TWO', ''))
    if not entry:
        return ''
    return entry.get('short') or entry.get('name') or ''


# ===== DB =====

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                company_name TEXT,
                rating TEXT,
                target_price REAL,
                current_price REAL,
                market TEXT,
                currency TEXT,
                created_at TEXT NOT NULL,
                full_json TEXT NOT NULL
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ticker ON analyses(ticker)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON analyses(created_at)")
        conn.commit()


def save_to_history(analysis: dict):
    try:
        data = {k: v for k, v in analysis.items() if k != 'price_history'}
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                """INSERT INTO analyses
                   (ticker, company_name, rating, target_price, current_price,
                    market, currency, created_at, full_json)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                (
                    analysis.get('ticker', ''),
                    analysis.get('company_name', ''),
                    analysis.get('overall_rating', ''),
                    analysis.get('target_price_12m'),
                    analysis.get('current_price'),
                    analysis.get('market', ''),
                    analysis.get('currency', ''),
                    datetime.now().isoformat(),
                    json.dumps(data, ensure_ascii=False),
                )
            )
            conn.commit()
    except Exception as e:
        print(f"[history] save failed: {e}")


init_db()


# ===== HELPERS =====

def detect_market(ticker):
    clean = ticker.upper().strip()
    if clean.isdigit() and 3 <= len(clean) <= 6:
        return 'TW', clean + '.TW'
    if '.TW' in clean or '.TWO' in clean:
        return 'TW', clean
    return 'US', clean


def fmt_num(n):
    if not n:
        return 'N/A'
    v = abs(n)
    if v >= 1e12:
        return f"{n/1e12:.2f}T"
    if v >= 1e9:
        return f"{n/1e9:.2f}B"
    if v >= 1e6:
        return f"{n/1e6:.2f}M"
    return f"{n:,.0f}"


def _yf_retry(func, max_attempts=3):
    """Call func() with exponential backoff on YFRateLimitError."""
    for attempt in range(max_attempts):
        try:
            return func()
        except YFRateLimitError:
            if attempt < max_attempts - 1:
                wait = 2 ** attempt
                print(f"[yfinance] rate limited, retrying in {wait}s ({attempt+1}/{max_attempts})")
                time.sleep(wait)
            else:
                raise
        except Exception:
            raise


def repair_json(raw: str) -> dict:
    """Four-layer JSON repair for Claude API responses."""

    def strip_fences(s):
        s = s.strip()
        if '```' in s:
            parts = s.split('```')
            for part in parts[1::2]:
                p = part.strip()
                if p.startswith('json\n') or p.startswith('json '):
                    p = p[4:].strip()
                if p.startswith('{'):
                    return p
        return s

    def clean(s):
        s = re.sub(r'//[^\n]*', '', s)          # remove // line comments
        s = re.sub(r',(\s*[}\]])', r'\1', s)     # remove trailing commas
        return s.strip()

    text = strip_fences(raw)

    # Layer 1: direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Layer 2: clean then parse
    try:
        return json.loads(clean(text))
    except json.JSONDecodeError:
        pass

    # Layer 3: extract {…} fragment + clean
    try:
        s, e = text.find('{'), text.rfind('}')
        if s != -1 and e > s:
            return json.loads(clean(text[s:e + 1]))
    except json.JSONDecodeError:
        pass

    raise ValueError(f"JSON解析失敗，三層修復均無效。AI輸出摘要：{raw[:400]}")


# ===== YFINANCE =====

def get_stock_data(yf_ticker):
    stock = yf.Ticker(yf_ticker)
    result = {'_data_quality': 'full', '_sources': {}}

    # Pre-fill Chinese company name for TW stocks via TWSE API
    if yf_ticker.endswith('.TW') or yf_ticker.endswith('.TWO'):
        tw_code = yf_ticker.replace('.TWO', '').replace('.TW', '')
        tw_name = get_tw_company_name(tw_code)
        if tw_name:
            result['_tw_verified_name'] = tw_name

    # --- info (with retry) ---
    try:
        info = _yf_retry(lambda: stock.info)
        for k in [
            'longName', 'shortName', 'currentPrice', 'regularMarketPrice',
            'marketCap', 'sector', 'industry', 'longBusinessSummary',
            'trailingPE', 'forwardPE', 'priceToBook', 'priceToSalesTrailing12Months',
            'beta', 'dividendYield', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow',
            'profitMargins', 'grossMargins', 'operatingMargins',
            'returnOnEquity', 'returnOnAssets', 'revenueGrowth', 'earningsGrowth',
            'totalDebt', 'totalCash', 'freeCashflow', 'currency', 'country',
            'targetMeanPrice', 'numberOfAnalystOpinions', 'recommendationKey',
        ]:
            result[k] = info.get(k)
        # For TW stocks: prefer TWSE verified Chinese name over yfinance English name
        if result.get('_tw_verified_name'):
            result['longName'] = result['_tw_verified_name']
        elif not result.get('longName') and result.get('shortName'):
            result['longName'] = result['shortName']
        result['_sources']['current_price'] = 'yahoo_finance'
    except Exception as e:
        result['_info_error'] = str(e)
        result['_data_quality'] = 'limited'
        # Still keep the verified name even if yfinance failed
        if result.get('_tw_verified_name'):
            result['longName'] = result['_tw_verified_name']

    # --- financials (with retry) ---
    try:
        fin = _yf_retry(lambda: stock.financials)
        if not fin.empty:
            rows = []
            for col in list(fin.columns)[:5]:
                yr = col.year if hasattr(col, 'year') else int(str(col)[:4])
                row = {'year': yr}
                for metric, key in [
                    ('revenue', 'Total Revenue'), ('gross_profit', 'Gross Profit'),
                    ('operating_income', 'Operating Income'), ('net_income', 'Net Income'),
                ]:
                    try:
                        row[metric] = float(fin.loc[key, col]) if key in fin.index else 0
                    except Exception:
                        row[metric] = 0
                rows.append(row)
            result['financials'] = rows
            result['_sources']['financials'] = 'yahoo_finance'
        else:
            result['financials'] = []
    except Exception:
        result['financials'] = []

    # --- cashflow (with retry) ---
    try:
        cf = _yf_retry(lambda: stock.cashflow)
        if not cf.empty:
            rows = []
            for col in list(cf.columns)[:5]:
                yr = col.year if hasattr(col, 'year') else int(str(col)[:4])
                row = {'year': yr}
                for metric, key in [
                    ('operating_cf', 'Operating Cash Flow'),
                    ('free_cf', 'Free Cash Flow'),
                ]:
                    try:
                        row[metric] = float(cf.loc[key, col]) if key in cf.index else 0
                    except Exception:
                        row[metric] = 0
                rows.append(row)
            result['cashflows'] = rows
            result['_sources']['cashflows'] = 'yahoo_finance'
        else:
            result['cashflows'] = []
    except Exception:
        result['cashflows'] = []

    # --- price history (with retry) ---
    try:
        hist = _yf_retry(lambda: stock.history(period="2y", interval="1mo"))
        result['price_history'] = [
            {'date': str(idx.date()), 'price': round(float(row['Close']), 2)}
            for idx, row in hist.iterrows()
        ]
        result['_sources']['price_history'] = 'yahoo_finance'
    except Exception:
        result['price_history'] = []

    return result


# ===== PROMPT =====

def build_annual_data_template(fin):
    """Build annual_data JSON array. Returns (data_str, source) tuple."""
    if fin:
        lines = []
        for y in fin[:5]:
            r = y.get('revenue') or 0
            gp = y.get('gross_profit') or 0
            oi = y.get('operating_income') or 0
            ni = y.get('net_income') or 0
            gm = round(gp / r * 100, 1) if r else 0
            om = round(oi / r * 100, 1) if r else 0
            nm = round(ni / r * 100, 1) if r else 0
            lines.append(
                f'      {{"year": "{y["year"]}", "revenue": {round(r / 1e6)}, '
                f'"net_income": {round(ni / 1e6)}, "gross_margin": {gm}, '
                f'"operating_margin": {om}, "net_margin": {nm}}}'
            )
        return ',\n'.join(lines), 'yahoo_finance'
    # Fallback example values
    return (
        '      {"year": "2024", "revenue": 35000, "net_income": 8500, "gross_margin": 55.0, "operating_margin": 25.0, "net_margin": 24.3},\n'
        '      {"year": "2023", "revenue": 33000, "net_income": 8000, "gross_margin": 54.0, "operating_margin": 24.0, "net_margin": 24.2},\n'
        '      {"year": "2022", "revenue": 30000, "net_income": 7500, "gross_margin": 53.0, "operating_margin": 23.5, "net_margin": 25.0},\n'
        '      {"year": "2021", "revenue": 27000, "net_income": 6500, "gross_margin": 52.0, "operating_margin": 22.5, "net_margin": 24.1},\n'
        '      {"year": "2020", "revenue": 23000, "net_income": 5500, "gross_margin": 51.0, "operating_margin": 21.0, "net_margin": 23.9}'
    ), 'example_fallback'


def build_prompt(ticker, market, d):
    is_tw = market == 'TW'
    fin = d.get('financials', [])
    data_note = d.get('_note', '')

    fin_lines = ""
    if fin:
        fin_lines = "年度財務（近5年）：\n"
        for y in fin:
            r = y.get('revenue') or 0
            gp = y.get('gross_profit') or 0
            oi = y.get('operating_income') or 0
            ni = y.get('net_income') or 0
            gm = gp / r * 100 if r else 0
            om = oi / r * 100 if r else 0
            nm = ni / r * 100 if r else 0
            fin_lines += (f"  {y['year']}: 營收={r/1e9:.2f}B, "
                          f"毛利率={gm:.1f}%, 營業利益率={om:.1f}%, "
                          f"淨利率={nm:.1f}%, 淨利={ni/1e9:.2f}B\n")

    cur_price = d.get('currentPrice') or d.get('regularMarketPrice') or 0
    pe_val = d.get('trailingPE') or 14.5
    pe_str = f"{pe_val:.1f}" if pe_val else "14.5"
    desc = str(d.get('longBusinessSummary') or '')[:500]
    data_quality_note = (
        f"\n⚠️ 注意：{data_note}\n請依據您的專業知識與訓練數據補充估算缺少的即時數字。\n"
        if data_note else ""
    )
    annual_data, _annual_source = build_annual_data_template(fin)
    company_name = d.get('longName') or d.get('shortName') or ticker
    name_lock = f'【已核實】此分析標的為：{ticker}，公司名稱：{company_name}。整份報告的 company_name 欄位必須填入「{company_name}」，禁止替換為其他公司名稱。'

    return f"""你是頂尖首席股票分析師，請分析 {ticker}（{company_name}）並回傳完整投資研究報告。

{name_lock}
{data_quality_note}
⚠️ 格式規則（必須遵守）：
1. 只回傳純JSON，不含任何 ``` markdown 符號或其他說明文字
2. 模板中的示例數字（如 185.50、7、35）都是佔位符，請替換為您對 {ticker} 的實際估算值
3. 字串欄位請填入真實分析內容，不要保留中文說明提示
4. 數字欄位必須是數字型別，不能是字串
5. 所有敘述性內容使用繁體中文
6. company_name 必須是「{company_name}」，不得修改

即時市場數據（部分可能為空，請依訓練知識補充）：
- 股價: {cur_price}  |  市值: {fmt_num(d.get('marketCap'))}
- 產業: {d.get('sector','N/A')} / {d.get('industry','N/A')}  |  計價: {'TWD' if is_tw else 'USD'}
- P/E: {d.get('trailingPE','N/A')}  |  P/B: {d.get('priceToBook','N/A')}
- 毛利率: {(d.get('grossMargins') or 0)*100:.1f}%  |  營業利益率: {(d.get('operatingMargins') or 0)*100:.1f}%  |  淨利率: {(d.get('profitMargins') or 0)*100:.1f}%
- ROE: {(d.get('returnOnEquity') or 0)*100:.1f}%  |  自由現金流: {fmt_num(d.get('freeCashflow'))}
- 52W高/低: {d.get('fiftyTwoWeekHigh','N/A')} / {d.get('fiftyTwoWeekLow','N/A')}
- 分析師目標價: {d.get('targetMeanPrice','N/A')}  |  評等: {d.get('recommendationKey','N/A')}
- YoY營收成長: {(d.get('revenueGrowth') or 0)*100:.1f}%

{fin_lines}
業務描述: {desc}

請回傳以下JSON（所有示例數值請替換為實際估算）：
{{
  "company_name": "{company_name}",
  "ticker": "{ticker}",
  "market": "{'TW' if is_tw else 'US'}",
  "currency": "{'TWD' if is_tw else 'USD'}",
  "current_price": {cur_price},
  "market_status_summary": "一句話精準描述目前市場熱度與產業拐點",
  "report_date": "{datetime.now().strftime('%Y-%m-%d')}",
  "overall_rating": "BUY",
  "target_price_12m": 185.50,
  "upside_potential": 12.5,
  "section1": {{
    "core_model": "核心商業模式深度描述，至少250字，包含主要業務線與收入結構",
    "revenue_breakdown": [
      {{"name": "業務線1名稱", "percentage": 35}},
      {{"name": "業務線2名稱", "percentage": 28}},
      {{"name": "業務線3名稱", "percentage": 22}},
      {{"name": "其他", "percentage": 15}}
    ],
    "tam_5yr_cagr": "TAM市場規模與5年CAGR詳細分析",
    "growth_opportunities": "具體擴張方向與第二成長曲線",
    "ai_tech_advantage": "AI或技術優勢深度分析",
    "tam_forecast": [
      {{"year": "2025", "value": 45}},
      {{"year": "2026", "value": 52}},
      {{"year": "2027", "value": 60}},
      {{"year": "2028", "value": 69}},
      {{"year": "2029", "value": 80}}
    ]
  }},
  "section2": {{
    "moat_score": 7,
    "moat_rationale": "外資犀利風格的核心給分理由（一句精準點評）",
    "brand_network": "品牌影響力與網路效應具體分析",
    "switching_cost": "轉換成本與定價權分析",
    "patents_tech": "專利與技術壁壘分析",
    "radar_scores": {{
      "brand": 8,
      "switching_cost": 7,
      "cost_advantage": 7,
      "patents": 9,
      "network_effects": 6
    }},
    "competitors": [
      {{"name": "{ticker}", "type": "本公司", "gross_margin": 55.0, "tech_advantage": "核心技術優勢", "moat_score": 7}},
      {{"name": "競爭對手A", "type": "國際對手", "gross_margin": 48.0, "tech_advantage": "技術優勢", "moat_score": 6}},
      {{"name": "競爭對手B", "type": "國內對手", "gross_margin": 42.0, "tech_advantage": "技術優勢", "moat_score": 5}}
    ]
  }},
  "section3": {{
    "revenue_trend": "營收成長趨勢深度分析，至少200字",
    "margin_analysis": "三率（毛利/營業/淨利）交叉走勢分析，至少200字",
    "cashflow_debt": "自由現金流與負債安全性分析",
    "roe_analysis": "ROE評估與產業比較",
    "health_verdict": "STRONG",
    "health_reason": "一針見血的財務體質核心判斷",
    "annual_data": [
{annual_data}
    ]
  }},
  "section4": {{
    "peer_comparison": "同業估值比較詳細分析",
    "dcf_analysis": "DCF折現現金流估值推演",
    "dcf_assumptions": {{
      "revenue_cagr_5yr": 12.5,
      "terminal_growth": 3.0,
      "wacc": 9.5,
      "implied_pe": 18.0
    }},
    "valuation_verdict": "FAIR",
    "rerating_catalyst": "重新估值機會與催化劑",
    "pe_band_data": {{
      "current_pe": {pe_str},
      "5yr_avg_pe": 18.2,
      "5yr_high_pe": 28.5,
      "5yr_low_pe": 11.3,
      "sector_avg_pe": 20.1
    }},
    "peer_data": [
      {{"name": "{ticker}", "pe": {pe_str}}},
      {{"name": "對手1", "pe": 22.3}},
      {{"name": "對手2", "pe": 18.5}},
      {{"name": "對手3", "pe": 15.8}},
      {{"name": "產業均值", "pe": 20.2}}
    ]
  }},
  "section5": {{
    "bull_point1": "多頭論點一（含具體數據支撐）",
    "bull_point1_data": "量化指標數據",
    "bull_point2": "多頭論點二（未被市場完全定價的催化劑）",
    "bull_point2_data": "量化指標數據",
    "bear_point1": "空頭論點一（含下行風險數據）",
    "bear_point1_data": "量化風險指標",
    "bear_point2": "空頭論點二（潛在侵蝕路徑）",
    "bear_point2_data": "量化風險指標",
    "analyst_conclusion": "首席分析師客觀中性結論，至少200字，不含糊"
  }},
  "section6": {{
    "bull_case": {{"condition": "多頭觸發條件描述", "target": 210.0, "pe": 22.0, "probability": 25}},
    "base_case": {{"condition": "基本情境描述", "target": 175.0, "pe": 18.0, "probability": 55}},
    "bear_case": {{"condition": "空頭觸發條件描述", "target": 130.0, "pe": 13.5, "probability": 20}},
    "catalysts": ["催化劑1", "催化劑2", "催化劑3", "催化劑4"],
    "risks": ["風險1", "風險2", "風險3", "風險4"]
  }},
  "section7": {{
    "short_term": "短期操作策略（1年內，含買點區間與觀察指標）",
    "long_term": "長期投資展望（5年以上，商業價值與護城河評估）",
    "rating": "BUY",
    "key_sentence": "外資備忘錄質感的核心決策金句（20字以內）",
    "buy_range_low": 155.0,
    "buy_range_high": 165.0
  }},
  "sandbox": {{
    "scenario1": {{
      "title": "關鍵原料價格衝擊",
      "trigger": "具體觸發條件描述",
      "impact_description": "詳細財務影響分析，至少150字",
      "margin_impact": -3.5,
      "eps_impact": -8.2,
      "valuation_impact": "估值修正邏輯"
    }},
    "scenario2": {{
      "title": "次世代產品滲透超預期",
      "trigger": "具體觸發條件描述",
      "impact_description": "詳細財務影響分析",
      "margin_impact": 4.2,
      "eps_impact": 12.5,
      "valuation_impact": "估值修正邏輯"
    }},
    "scenario3": {{
      "title": "競爭格局與地緣政治衝擊",
      "trigger": "具體觸發條件描述",
      "impact_description": "詳細財務影響分析",
      "margin_impact": -5.0,
      "eps_impact": -15.0,
      "valuation_impact": "估值修正邏輯"
    }}
  }}
}}"""


# ===== DATA PROVENANCE =====

def build_data_sources(stock_data):
    src = stock_data.get('_sources', {})
    fin = stock_data.get('financials', [])
    _, annual_source = build_annual_data_template(fin)
    limited = stock_data.get('_data_quality') == 'limited'
    return {
        'current_price': src.get('current_price', 'claude_ai' if limited else 'unknown'),
        'annual_data': annual_source,
        'cashflows': src.get('cashflows', 'claude_ai' if limited else 'unknown'),
        'price_history': src.get('price_history', 'claude_ai' if limited else 'unknown'),
        'target_price_12m': 'claude_ai',
        'overall_rating': 'claude_ai',
        'moat_score': 'claude_ai',
    }


def validate_analysis(analysis, stock_data, data_sources):
    warnings = []
    price = analysis.get('current_price') or 0
    if not price or float(price) <= 0:
        warnings.append({'field': 'current_price', 'message': '股價資料異常，請確認股票代碼是否正確'})
    if data_sources.get('annual_data') == 'example_fallback':
        warnings.append({'field': 'annual_data', 'message': '財務歷史數據為範例預設值，非真實財報，僅供參考'})
    if stock_data.get('_data_quality') == 'limited':
        warnings.append({'field': 'market_data', 'message': '即時市場數據抓取受限，部分數值由 AI 依訓練資料填補，可能非最新'})
    return warnings


# ===== ROUTES =====

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        body = request.json or {}
        ticker_raw = (body.get('ticker') or '').strip().upper()
        api_key = body.get('api_key') or os.getenv('ANTHROPIC_API_KEY', '')

        if not ticker_raw:
            return jsonify({'error': '請輸入股票代碼'}), 400
        if not api_key:
            return jsonify({'error': '請提供 Anthropic API Key'}), 400

        market, yf_ticker = detect_market(ticker_raw)
        data = get_stock_data(yf_ticker)

        if not data.get('longName') and not data.get('currentPrice'):
            data['_note'] = '即時數據獲取受限，Claude 將依訓練知識進行分析'

        prompt = build_prompt(ticker_raw, market, data)

        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=8000,
            system=(
                "你是一位在華爾街與外資券商擁有20年經驗的頂尖首席股票分析師。"
                "只回傳純JSON，不含任何markdown符號（```）或多餘說明文字。"
                "JSON模板中的示例數字（如185.50、7）都必須替換為你的實際分析估算值。"
                "所有敘述性文字使用繁體中文，數字欄位必須是數字型別。"
            ),
            messages=[{"role": "user", "content": prompt}]
        )

        raw = msg.content[0].text.strip()
        analysis = repair_json(raw)
        analysis['price_history'] = data.get('price_history', [])

        # Enforce verified company name — prevent AI from hallucinating a different company
        verified_name = data.get('longName') or data.get('shortName')
        if verified_name and analysis.get('company_name') != verified_name:
            analysis['company_name'] = verified_name

        data_sources = build_data_sources(data)
        data_warnings = validate_analysis(analysis, data, data_sources)
        analysis['data_sources'] = data_sources
        analysis['data_warnings'] = data_warnings

        save_to_history(analysis)

        return jsonify({'success': True, 'data': analysis})

    except anthropic.AuthenticationError:
        return jsonify({'error': 'Anthropic API Key 無效，請確認您的金鑰是否正確'}), 401
    except ValueError as e:
        return jsonify({'error': f'AI 回傳格式解析失敗，請重試。\n{str(e)[:200]}'}), 500
    except Exception as e:
        return jsonify({'error': f'分析失敗：{str(e)}'}), 500


@app.route('/api/history', methods=['GET'])
def list_history():
    ticker_filter = request.args.get('ticker', '').strip().upper()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            if ticker_filter:
                rows = conn.execute(
                    "SELECT id,ticker,company_name,rating,target_price,current_price,market,currency,created_at "
                    "FROM analyses WHERE UPPER(ticker)=? ORDER BY created_at DESC",
                    (ticker_filter,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT id,ticker,company_name,rating,target_price,current_price,market,currency,created_at "
                    "FROM analyses ORDER BY created_at DESC"
                ).fetchall()
        return jsonify({'success': True, 'data': [dict(r) for r in rows]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history/<int:record_id>', methods=['GET'])
def get_history(record_id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            row = conn.execute(
                "SELECT full_json FROM analyses WHERE id=?", (record_id,)
            ).fetchone()
        if not row:
            return jsonify({'error': '找不到此分析記錄'}), 404
        return jsonify({'success': True, 'data': json.loads(row[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history/<int:record_id>', methods=['DELETE'])
def delete_history(record_id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("DELETE FROM analyses WHERE id=?", (record_id,))
            conn.commit()
        if cur.rowcount == 0:
            return jsonify({'error': '找不到此分析記錄'}), 404
        return jsonify({'success': True, 'message': '已刪除'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(debug=True, port=port)
