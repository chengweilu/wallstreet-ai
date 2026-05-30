## Context

報告頁面由 Flask 渲染的單頁應用（SPA）組成，圖表使用 Chart.js 4.x 繪製於 `<canvas>` 元素。目前無任何匯出功能。`html2canvas` 是業界標準的純前端截圖函式庫，可捕捉包含 canvas 的 DOM 節點，不需後端支援。

## Goals / Non-Goals

**Goals:**
- 一鍵將整份報告（含所有 Chart.js 圖表）渲染為 PNG 並觸發瀏覽器下載
- 支援完整長頁面捕捉（不只是視窗可見區域）
- 檔名包含 ticker 與日期，方便管理

**Non-Goals:**
- PDF 匯出
- 直接上傳到 LINE（需使用者手動傳送）
- 後端生成截圖（純前端實作）
- 歷史報告的截圖匯出（僅限即時報告頁）

## Decisions

**使用 html2canvas（CDN）**
- 理由：零後端依賴，對 `<canvas>` 元素有原生支援，可捕捉 Chart.js 渲染結果
- 替代方案：`dom-to-image`（對 canvas 支援較差）、後端 puppeteer（過重）
- 載入方式：`<script>` CDN，僅在 `#report` 顯示時才啟動，不影響頁面載入

**捕捉對象：`#report` 節點**
- 包含所有 section（報告標頭、七大章節、AI Sandbox）
- 排除 navbar，使截圖更簡潔

**按鈕位置：報告頁頂部操作列（`#report` 的 `.report-actions`）**
- 與現有「新分析」按鈕同排，視覺一致

## Risks / Trade-offs

- [html2canvas 跨域圖片] 若有外部圖片資源可能失敗 → 目前報告無外部圖片，風險低
- [長頁面記憶體] 非常長的報告可能消耗較多記憶體 → 屬正常範圍，現代瀏覽器可承受
- [字型渲染] CDN 字型可能在截圖中稍有差異 → 視覺影響輕微，可接受
