## 1. 後端技術指標 API（app.py）

- [x] 1.1 新增 `calc_technical_indicators(yf_ticker)` 函式：取 yfinance 日線數據（`history(period="6mo")`），計算並回傳含 ma20/ma50/ma200/rsi/macd/signal/hist/price_with_ma 的 dict
- [x] 1.2 在函式中實作 MA 計算：`df['ma20'] = df['Close'].rolling(20).mean()`，同理 ma50/ma200
- [x] 1.3 實作 RSI(14)：`delta = df['Close'].diff(); gain = delta.clip(lower=0).ewm(com=13).mean(); loss = -delta.clip(upper=0).ewm(com=13).mean(); rsi = 100 - 100/(1+gain/loss)`
- [x] 1.4 實作 MACD：`ema12 = df['Close'].ewm(span=12).mean(); ema26 = df['Close'].ewm(span=26).mean(); macd = ema12 - ema26; signal = macd.ewm(span=9).mean(); hist = macd - signal`
- [x] 1.5 實作 `calc_signal_score(data)` 函式：依 5 條件加權計算 0–100 分數與 signal_label 文字
- [x] 1.6 組裝 `price_with_ma` 陣列：最後 90 筆，每筆 `{"date": str, "close": float, "ma20": float|null, "ma50": float|null, "ma200": float|null}`
- [x] 1.7 新增 Flask route `@app.route('/api/technical/<ticker>')` 呼叫 `calc_technical_indicators`，捕捉例外回傳 `{"success": false, "error": str}`

## 2. 前端 Navbar 加入技術面連結（index.html）

- [x] 2.1 在 navbar `.nav-links` 中加入 `<a href="#sec8" class="nav-link" data-sec="sec8">技術面</a>`

## 3. 前端 Section 8 HTML 結構（index.html）

- [x] 3.1 在 Section 7（`#sec7`）的 `</section>` 之後加入 `<section class="sec" id="sec8">` 技術面 section 骨架
- [x] 3.2 在 section 內加入信號摘要卡（`id="tech-summary-card"`）：顯示總分、label、五條件 checklist（初始為 skeleton）
- [x] 3.3 加入均線疊加圖卡（`class="chart-card"`）：含 `<canvas id="chart-ma-overlay"></canvas>`
- [x] 3.4 加入三個指標小卡（MA 狀態、RSI、MACD），初始顯示 skeleton-line

## 4. 前端 JS 渲染邏輯（index.html）

- [x] 4.1 新增 `fetchTechnicalAnalysis(ticker)` async 函式：呼叫 `/api/technical/<ticker>`，成功後呼叫 `renderTechnicalSection(data)`，失敗後顯示錯誤提示
- [x] 4.2 在 `renderReport(d)` 的 `show('report')` 之後加入 `setTimeout(() => fetchTechnicalAnalysis(d.ticker), 500)`（非同步，不阻塞主報告）
- [x] 4.3 新增 `renderTechnicalSection(data)` 函式：填入信號摘要卡數值、五條件 ✅/❌、MA/RSI/MACD 數值與顏色
- [x] 4.4 在 `renderTechnicalSection` 中加入 Chart.js 均線疊加圖渲染：price/ma20/ma50/ma200 四條折線，顏色依設計決策
- [x] 4.5 在 `destroyCharts()` 中加入 `chart-ma-overlay` canvas 的圖表銷毀邏輯

## 5. 樣式（index.html CSS）

- [x] 5.1 新增 `.tech-signal-card` CSS：仿照 `.card` 樣式，加入信號燈顏色變數
- [x] 5.2 新增 `.signal-score-big` CSS：大字體顯示技術評分（仿照 `.score-big`）
- [x] 5.3 新增 `.signal-checklist` CSS：五條件 checklist 的排版樣式
- [x] 5.4 新增 `.tech-indicator-grid` CSS：三個小指標卡的 grid 排版（`grid-template-columns: repeat(3, 1fr)`）

## 6. 驗證

- [x] 6.1 用 `curl http://127.0.0.1:5001/api/technical/AAPL` 確認 API 回傳正確 JSON 含所有欄位
- [x] 6.2 分析 AAPL，確認主報告顯示後 Section 8 自動非同步載入
- [x] 6.3 確認均線圖正確渲染，四條折線顏色正確
- [x] 6.4 確認信號摘要卡的 ✅/❌ 與評分邏輯正確
- [x] 6.5 分析一支台股（如 2330），確認 TW 市場技術分析也正常運作
