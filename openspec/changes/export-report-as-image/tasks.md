## 1. 載入 html2canvas（`templates/index.html`）

- [x] 1.1 在 `</body>` 前新增 `<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js">` CDN 標籤

## 2. 新增「下載圖片」按鈕（`templates/index.html`）

- [x] 2.1 在報告頁頂部操作列（`#btn-new` 同排）新增 `<button id="btn-export-img" onclick="exportReportAsImage()">📷 下載圖片</button>`
- [x] 2.2 新增按鈕 CSS 樣式（與 `.btn-go-landing` 視覺一致，amber 色調）

## 3. 實作 `exportReportAsImage()` 函數（`templates/index.html`）

- [x] 3.1 實作 `exportReportAsImage()`：按鈕改為「⏳ 生成中...」並 `disabled`
- [x] 3.2 呼叫 `html2canvas(document.getElementById('report'), { scale: 2, useCORS: true, scrollY: -window.scrollY })` 捕捉完整報告
- [x] 3.3 將 canvas 轉為 PNG dataURL，建立 `<a>` 標籤觸發下載，檔名格式 `TICKER_YYYYMMDD.png`（從 `currentAnalysis` 取 ticker）
- [x] 3.4 下載完成後恢復按鈕文字與啟用狀態；捕捉錯誤時 `alert('圖片匯出失敗，請稍後再試')` 並恢復按鈕

## 4. 收尾

- [x] 4.1 重啟 Flask，分析一支股票後點擊「下載圖片」，確認 PNG 下載且圖表完整顯示
