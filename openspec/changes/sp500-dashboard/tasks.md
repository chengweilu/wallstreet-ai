## 1. 建立專案目錄結構

- [x] 1.1 建立 `/Users/cwluu/Desktop/Louie_claude/sp500_dashboard/` 及子目錄 `src/`、`data/`
- [x] 1.2 建立 `requirements.txt`（yfinance, pandas, requests, python-dotenv）
- [x] 1.3 建立 `run.sh`：執行 `python3 src/fetch_data.py`，成功後輸出「✅ 數據已更新，請雙擊 index.html」

## 2. 後端：S&P 500 成分股抓取（`src/fetch_data.py`）

- [x] 2.1 實作 `get_sp500_tickers()` — `pd.read_html` 抓 Wikipedia，失敗則 fallback 至內建 50 支代表性 ticker
- [x] 2.2 用 yfinance 批次抓取所有成分股的 `marketCap`、`netIncome`、`sector`、`avgVolume`（每批 50 支，sleep 0.5s 避免限速）
- [x] 2.3 計算 `sp500_total_market_cap`（所有成分股市值總和）

## 3. 後端：雙源驗證（`src/fetch_data.py`）

- [x] 3.1 實作 `get_sec_net_income(ticker)` — 呼叫 SEC Edgar `/api/xbrl/companyfacts/{cik}` 取最新季報 `NetIncomeLoss`（需先取得 CIK mapping）
- [x] 3.2 實作 `validate_data(ticker, yf_val, sec_val)` — 計算誤差，> 1% 記錄至 audit_log，回傳最終採用值
- [x] 3.3 對市值前 30 名執行雙源驗證（節省 API quota），生成 `data/audit_log.json`

## 4. 後端：量化指標計算（`src/fetch_data.py`）

- [x] 4.1 篩選邊緣股：市值排名倒數 10 名 + 虧損（netIncome < 0），計算剔除後各板塊權重變化
- [x] 4.2 計算機構持股比例：yfinance `stock.institutional_holders`，取前 10 大機構持股總比例
- [x] 4.3 計算 Days to Cover：`passive_buy = 6e12 * (market_cap / total_market_cap)`；`days_to_cover = passive_buy / (avgVolume * current_price)`
- [x] 4.4 計算板塊落差：比較 S&P 500 各板塊權重 vs 全市場（Russell 3000 近似，用 yfinance 板塊總市值）

## 5. 後端：K 線數據與輸出（`src/fetch_data.py`）

- [x] 5.1 取 Days to Cover 排名前 3 的候選股，抓取 2 年日線 OHLCV（yfinance）
- [x] 5.2 計算 50 日 SMA、200 日 SMA、RSI（14 日）、MACD（12/26/9）
- [x] 5.3 計算策略買點區間（52 周低點 × 1.05 至 × 1.15）與防守停損價（52 周低點 × 0.97）
- [x] 5.4 組裝 `dashboard_data.json`（含 meta、edge_stocks、candidates、sector_diff、top3_ohlcv 五個頂層 key）
- [x] 5.5 將 JSON 內嵌至 `index.html` 的 `window.DASHBOARD_DATA = {...}` 變數（`fetch_data.py` 讀取 index.html 模板，替換佔位符後寫出）

## 6. 前端：頁面架構與頂部看板（`index.html`）

- [x] 6.1 建立 `index.html` 骨架：CDN 載入 Tailwind CSS、Alpine.js、Plotly.js；`<script>window.DASHBOARD_DATA = __DATA_PLACEHOLDER__;</script>`
- [x] 6.2 實作頂部 Grid 看板：市值門檻、邊緣股數量、預估調整日期、資料更新時間 4 張卡片

## 7. 前端：候選股動態矩陣（`index.html`）

- [x] 7.1 用 Alpine.js `x-data` 實作表格狀態（排序欄位、方向、搜尋字串）
- [x] 7.2 實作表頭點擊排序（`@click` toggle asc/desc + `x-text` 箭頭）
- [x] 7.3 實作搜尋框 `x-model` 即時過濾（ticker 或 sector 包含字串）
- [x] 7.4 表格欄位：Ticker、公司名、板塊、市值（億）、Days to Cover、機構持股%、是否邊緣股（標籤）

## 8. 前端：板塊落差圖 + Days to Cover 圖（`index.html`）

- [x] 8.1 實作 `renderSectorChart()` — Plotly 水平長條圖，x 軸為板塊落差%，hover 顯示具體數值
- [x] 8.2 實作 `renderDaysToCoverChart()` — Plotly 水平長條圖，依 days_to_cover 降冪，top 10 候選股

## 9. 前端：K 線圖 + 技術指標（`index.html`）

- [x] 9.1 建立 3 個 Tab（前 3 名候選股），Alpine.js 管理 `activeTab` 狀態
- [x] 9.2 實作 `renderCandlestick(ticker)` — Plotly candlestick + 50/200 SMA 疊加線圖（subplot row 1）
- [x] 9.3 實作 `renderRSI(ticker)` — Plotly 折線圖（subplot row 2），30/70 超買超賣水平線
- [x] 9.4 實作 `renderMACD(ticker)` — Plotly bar（histogram）+ 折線（signal）（subplot row 3）
- [x] 9.5 在 K 線圖加入策略買點半透明矩形（`shape` 類型）與停損水平線（`shape` 類型）
- [x] 9.6 三個 subplot 共用同一個 x 軸（linked zoom），`Tab` 切換時重新渲染

## 10. 前端：審計日誌 Modal（`index.html`）

- [x] 10.1 建立 Modal HTML 結構（Tailwind fixed overlay），Alpine.js `x-show` 控制顯示
- [x] 10.2 在 Modal 內渲染 `audit_log` 表格（ticker、數據來源、yf/sec 數值、誤差%、校正狀態）
- [x] 10.3 點擊 overlay 或 ✕ 按鈕關閉 Modal

## 11. 收尾與測試

- [x] 11.1 執行 `python3 src/fetch_data.py`，確認生成 `data/dashboard_data.json` 與 `data/audit_log.json`
- [x] 11.2 雙擊 `index.html`（或用 `python3 -m http.server 8080`），確認頁面正常顯示所有區塊
- [x] 11.3 測試表格排序與搜尋功能
- [x] 11.4 測試 K 線圖 Tab 切換與縮放
- [x] 11.5 測試審計日誌 Modal 開關
