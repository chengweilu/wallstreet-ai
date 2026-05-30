## Why

WallStreet AI 目前只有基本面分析（7 大維度），缺少技術面觀點。技術分析（MA 均線、RSI、MACD）是散戶與短線交易者最常參考的工具，引入 `algo-trading` skill 的量化指標方法論，新增技術面分析頁籤，讓報告涵蓋面更完整，同時提供具體買賣信號參考。

## What Changes

- 新增 Flask API 路由 `/api/technical/<ticker>`：從 yfinance 取 90 天日線數據，計算 MA20/MA50/MA200、RSI(14)、MACD 並回傳
- 新增前端「技術面」Section（Section 8 或獨立卡片）：顯示均線多空排列、RSI 信號、MACD 方向
- 新增技術信號摘要卡片：統整「技術面綜合評分」（0–100）與「技術買賣建議」
- 在 Landing 的分析流程中，報告渲染後自動呼叫技術分析 API 並顯示結果

## Capabilities

### New Capabilities
- `technical-indicators-api`: Flask 後端 `/api/technical/<ticker>` 計算並回傳 MA/RSI/MACD
- `technical-analysis-ui`: 前端新增技術面卡片，顯示指標數值、信號方向與均線圖
- `technical-signal-summary`: 綜合多個技術指標給出總分與建議（強多/偏多/中性/偏空/強空）

### Modified Capabilities

## Impact

- `app.py` 新增一個 route 與技術指標計算函式（使用已有的 yfinance）
- `index.html` 新增 Section 8 HTML + JS 渲染函式 + API 呼叫
- 不影響現有 Section 1–7 的任何邏輯
- yfinance 已是現有依賴，不需新增套件（RSI/MACD 手算，不依賴 ta-lib）
