## Context

S&P 500 成分股每季調整，被動型 ETF（規模約 6 兆美元）必須買入新納入個股，形成可預測的資金流。本儀表板透過量化計算「Days to Cover」幫助使用者在被動買盤發生前佈局。

## Goals / Non-Goals

**Goals:**
- 雙擊 `index.html` 即可使用（不需 Flask、Node.js 或任何伺服器）
- `fetch_data.py` 單次執行產出所有所需 JSON，前端純讀取
- K 線圖支援放大縮小、技術指標互動

**Non-Goals:**
- 即時自動更新（使用者需手動重跑 `fetch_data.py`）
- 整合進現有 stock_analyzer Flask app
- 付費數據源（全用免費 API：yfinance、SEC Edgar EDGAR API）

## Decisions

**目錄結構**
```
sp500_dashboard/
├── src/
│   └── fetch_data.py       # 數據抓取、驗證、計算
├── data/
│   ├── dashboard_data.json # 主要數據輸出
│   └── audit_log.json      # 驗證日誌
├── index.html              # 靜態儀表板
├── run.sh                  # 一鍵啟動
└── requirements.txt
```

**雙源驗證策略**
- 主源：yfinance（`stock.info` 的 `marketCap`、`netIncome`）
- 副源：SEC Edgar EDGAR API（`/api/xbrl/companyfacts`，取 `us-gaap/NetIncomeLoss` 最新季報）
- 誤差計算：`abs(yf_val - sec_val) / sec_val > 0.01` → 記錄警告並以 SEC 數據為主

**S&P 500 成分股來源**
- 從 Wikipedia S&P 500 頁面抓取（`pd.read_html`）→ 取得 ticker list
- 若抓取失敗，fallback 至預存的 500 個 ticker 清單

**Days to Cover 公式**
```
passive_fund_aum = 6_000_000_000_000  # 6兆美元
weight = stock_market_cap / sp500_total_market_cap
estimated_passive_buy = passive_fund_aum * weight
days_to_cover = estimated_passive_buy / avg_30d_volume_usd
```

**前端技術棧（CDN only）**
- Tailwind CSS 3.x：UI 樣式
- Alpine.js 3.x：輕量互動（排序、搜尋、Tab 切換、Modal）
- Plotly.js 2.x：K 線圖、長條圖、RSI/MACD

**本地 JSON 讀取限制**
瀏覽器 `fetch('data/dashboard_data.json')` 在 `file://` 協議下因 CORS 可能被阻擋。解法：
1. 使用 `<script>` 標籤 inline 方式嵌入 JSON（`fetch_data.py` 把 JSON 寫入 `<script>` 區塊內的 JS 變數）
2. 或提供 `python3 -m http.server 8080` 指令讓使用者啟動簡易伺服器

選擇方案 1（內嵌 JS 變數），真正做到雙擊即開。

## Risks / Trade-offs

- [SEC Edgar API 速率限制] 500 支股票 × 2 個 API = 大量請求 → 加入 `time.sleep(0.1)` 節流，限制驗證只做前 50 名候選股
- [Wikipedia 頁面結構變更] `pd.read_html` 解析可能失敗 → fallback 至預存清單
- [K 線圖數據量] 2 年日線 × 3 支股票 → yfinance 批次抓取，合理
