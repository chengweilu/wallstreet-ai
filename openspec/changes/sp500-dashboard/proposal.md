## Why

現有股票分析系統針對單一股票進行深度研究，但缺乏對 S&P 500 整體結構的宏觀視角——例如哪些股票面臨納入/剔除邊緣、被動資金對個股的推升力道、以及技術面買賣時機。本提案建立一個完全獨立的量化儀表板，不依賴伺服器，雙擊即開，讓使用者快速掌握 S&P 500 的前瞻動態。

## What Changes

**新建獨立專案目錄 `sp500_dashboard/`**（與 `stock_analyzer/` 同層）：

- `src/fetch_data.py`：Python 後端資料驗證與量化計算腳本
  - 雙源（yfinance + SEC Edgar）交叉比對市值與淨利，誤差 > 1% 觸發校正
  - 篩選 S&P 500 邊緣股（市值倒數 10 名 + 虧損股）
  - 計算機構持股比例、預估被動買入金額、Days to Cover
  - 輸出 `data/dashboard_data.json` + `data/audit_log.json`
- `index.html`：純靜態單頁儀表板（CDN only，無需伺服器）
  - 頂部核心數據看板（市值門檻、候選股數量、預估調整日期）
  - 候選股動態矩陣（表格排序、搜尋過濾）
  - 板塊權重落差圖 + Days to Cover 長條圖（Plotly.js）
  - 前 3 名候選股 K 線圖 + 50/200 SMA + RSI + MACD（Tab 切換）
  - 策略買點區間標注、防守停損價
  - 數據審計日誌彈窗（Modal）
- `run.sh`：一鍵啟動腳本（執行 fetch_data.py → 確認 JSON → 提示完成）
- `requirements.txt`：Python 依賴清單

## Capabilities

### New Capabilities
- `data-pipeline`: 雙源驗證、邊緣股篩選、Alpha 計算（機構持股、被動資金、Days to Cover）
- `dashboard-ui`: 互動式儀表板，含表格排序/搜尋、Plotly 圖表、K 線 + 技術指標、審計 Modal

### Modified Capabilities
（此為全新獨立專案，不修改既有 stock_analyzer）

## Impact

- 新建目錄：`/Users/cwluu/Desktop/Louie_claude/sp500_dashboard/`
- Python 依賴：`yfinance`, `pandas`, `requests`（已在 stock_analyzer 中使用，複用即可）
- 無後端伺服器：`index.html` 直接讀取本機 JSON 檔案（fetch 本地路徑）
- 不影響現有 stock_analyzer 任何功能
