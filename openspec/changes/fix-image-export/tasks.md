## 1. 修復變數名稱錯誤（`templates/index.html`）

- [x] 1.1 將 `exportReportAsImage()` 中的 `currentAnalysis` 改為 `currentData`

## 2. 驗證 html2canvas 基本功能

- [x] 2.1 在瀏覽器主控台執行 `typeof html2canvas`，確認回傳 `"function"`（而非 `"undefined"`）
- [x] 2.2 在主控台執行 `html2canvas(document.getElementById('report'), {scale:1, logging:true})` 並確認無 JS 錯誤拋出

## 3. 端對端測試：圖片匯出完整流程

- [x] 3.1 重啟 Flask，開啟 http://127.0.0.1:5000，輸入 QCOM 完成分析，等待報告完整顯示
- [x] 3.2 點擊 Navbar「📷 下載圖片」，確認按鈕變為「⏳ 生成中...」且無法再次點擊
- [x] 3.3 等待下載完成，確認瀏覽器下載列出現 `QCOM_YYYYMMDD.png` 檔案
- [x] 3.4 開啟下載的 PNG，確認：報告完整（含 7 個章節標題）、Chart.js 圖表有圖像（雷達圖、財務圖、本益比圖等）、文字清晰可讀
- [x] 3.5 確認按鈕恢復為「📷 下載圖片」且可再次點擊

## 4. 邊界情況測試

- [x] 4.1 從歷史記錄重新載入報告後點「📷 下載圖片」，確認同樣可正常下載
- [x] 4.2 確認 PNG 檔名 ticker 正確（與報告頁顯示一致）
