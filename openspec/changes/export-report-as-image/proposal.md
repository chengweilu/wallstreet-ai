## Why

使用者完成股票分析後，希望能一鍵將報告（含圖表、評等、財務數據）匯出為 PNG 圖片，方便直接傳送到 LINE 聊天室分享。目前報告只能在瀏覽器查看，無法快速轉為可分享的圖片格式。

## What Changes

- 在報告頁面新增「下載圖片」按鈕
- 使用 `html2canvas` 將整份報告（含所有 Chart.js 圖表）渲染為長截圖
- 自動以 `TICKER_YYYYMMDD.png` 命名並觸發下載
- 匯出期間顯示進度提示，完成後恢復正常

## Capabilities

### New Capabilities
- `report-image-export`: 將報告頁面截圖並下載為 PNG，支援完整長頁面與 canvas 圖表捕捉

### Modified Capabilities
（無）

## Impact

- `templates/index.html`：新增按鈕 HTML、CSS 樣式、`exportReportAsImage()` JS 函數
- 新增前端依賴：`html2canvas`（CDN 載入，無需後端變更）
- 不影響後端 `app.py` 或資料庫
