## Context

`index.html` 有一個全域變數 `currentData`（在 `startAnalysis()` 執行成功後被賦值為 `json.data`），包含分析結果物件。`exportReportAsImage()` 錯誤地使用了 `currentAnalysis`，這個變數從未被宣告，導致 `ReferenceError`。

## Goals / Non-Goals

**Goals:**
- 修正變數名稱，讓 PNG 檔名能正確帶入 ticker（例如 `QCOM_20260528.png`）
- 驗證整個匯出流程可在真實瀏覽器環境成功執行：從點按鈕到 PNG 下載完成

**Non-Goals:**
- 自動化瀏覽器測試（Selenium / Playwright）
- 後端截圖功能

## Decisions

**手動測試為主**
- 圖片匯出是純前端視覺功能，需要真實瀏覽器環境
- 測試步驟明確、可重現，手動執行即可驗證

**測試要涵蓋的驗證點**
1. 按鈕點擊後顯示「⏳ 生成中...」且暫時禁用
2. PNG 下載觸發（瀏覽器下載列顯示或儲存對話框）
3. 下載檔名格式正確（`TICKER_YYYYMMDD.png`）
4. 開啟 PNG：所有 7 個章節可見，Chart.js 圖表完整呈現（不是空白方塊）
5. 按鈕恢復正常狀態

## Risks / Trade-offs

- [Safari canvas 尺寸上限] Safari 對大型 canvas 有 16.7MB 限制 → `scale: 1.5` 已降低風險，若仍失敗可降至 `scale: 1`
- [字型可能在截圖中略有差異] CDN Google Fonts 在 html2canvas 中可能 fallback 到系統字型 → 視覺影響輕微，可接受
