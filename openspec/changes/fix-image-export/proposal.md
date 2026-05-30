## Why

`exportReportAsImage()` 函數參照了不存在的全域變數 `currentAnalysis`，實際應為 `currentData`，導致每次點擊「下載圖片」均拋出 `ReferenceError` 並顯示匯出失敗。需修復此錯誤，並建立完整的端對端測試流程，確保截圖功能真正可用後才提交。

## What Changes

- 將 `exportReportAsImage()` 中的 `currentAnalysis` 改為 `currentData`
- 建立手動測試清單，驗證圖片匯出的完整流程（觸發、等待、下載、圖片內容）
- 確認 Chart.js 圖表在截圖中完整顯示

## Capabilities

### New Capabilities
（無新功能，僅修復現有功能）

### Modified Capabilities
- `report-image-export`：修復 `currentAnalysis` 變數名錯誤，確保 ticker 能正確帶入檔名

## Impact

- `templates/index.html`：`exportReportAsImage()` 函數單一行修改
- 不影響後端、資料庫、其他 JS 函數
