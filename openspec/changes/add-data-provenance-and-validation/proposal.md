## Why

報告中部分數據不正確（例如股價、淨利），使用者難以判斷哪些是真實市場數據、哪些是 AI 估算。根本原因是：yfinance 抓取失敗時，Claude 會用訓練資料填補，但沒有任何標示說明數據來源；另外當財務數據取不到時，程式會靜默使用硬編碼的範例數字，使用者無從得知。

## What Changes

- 後端 `app.py` 新增 `data_sources` 物件（每個關鍵欄位標明來源：`yahoo_finance` / `claude_ai` / `example_fallback`）
- 後端新增 `data_warnings` 列表（股價為 0 / 財務數據全為 0 等異常時記錄警告）
- 後端將 `_data_quality`（`full` / `limited`）一起回傳至前端
- 前端在報告關鍵數字旁顯示來源徽章（`YF` = Yahoo Finance、`AI` = Claude 估算、`⚠` = 範例數據）
- 前端報告底部新增「資料品質摘要」卡片，匯總數據來源與任何警告

## Capabilities

### New Capabilities
- `data-provenance`: 標示每筆關鍵數據的來源，並在前端以徽章呈現
- `data-validation`: 後端驗證關鍵欄位合理性，前端顯示警告

### Modified Capabilities
（無需求層級變更）

## Impact

- `app.py`：`get_stock_data()` 新增來源追蹤；`analyze()` route 新增驗證邏輯，回傳 `data_sources` 與 `data_warnings`
- `templates/index.html`：報告頁新增來源徽章 CSS + JS 渲染邏輯；底部新增資料品質摘要區塊
- 不影響 API 契約既有欄位，僅新增欄位（向後相容）
