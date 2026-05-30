## Why

報告生成最後一步（`/api/analyze` 回傳後 JSON 解析）會因 Claude 回傳非標準 JSON（如中文「目標價數字」佔位符、數字夾雜文字、trailing comma、截斷輸出）而導致 `json.JSONDecodeError` 靜默失敗。yfinance 被限速後也未重試，導致空數據送往 Claude，產出品質差的報告或 prompt 注入無效佔位符。現在需要確認 QCOM 端對端可以正常執行並顯示報告。

## What Changes

- **JSON 解析強化**：加入多層 fallback 解析邏輯，先嘗試 `json.loads`，失敗時用正則修復常見問題（移除 trailing comma、修復中文佔位符、處理截斷），最後回傳結構化錯誤讓使用者知道具體原因
- **yfinance 自動重試**：加入 exponential backoff 重試（最多 3 次，間隔 2/4/8 秒），捕捉 `YFRateLimitError`，確保拿到 QCOM 的即時財務數據
- **Prompt 數字佔位符修正**：prompt 中 `目標價數字` 等中文佔位符會被 Claude 直接複製進 JSON，改為明確的英文鍵名與範例數字，避免 LLM 誤解
- **端對端測試腳本**：新增 `test_qcom.py`，直接呼叫 Flask API `/api/analyze`，驗證 JSON 結構完整性，並打印摘要確認報告生成成功
- **前端錯誤細化**：在 `index.html` 顯示更具體的錯誤訊息，區分「網路錯誤」「API Key 無效」「JSON 解析失敗」，讓使用者知道如何處置

## Capabilities

### New Capabilities
- `json-repair`: 多層 JSON fallback 解析，處理 Claude 常見的非標準輸出
- `yfinance-retry`: yfinance 限速自動重試機制
- `e2e-test`: QCOM 端對端測試腳本，驗證報告生成完整流程

### Modified Capabilities
<!-- 無需修改既有 spec -->

## Impact

- **`app.py`**：修改 `get_stock_data()`（加重試）、`analyze()` route（加 JSON repair）、`build_prompt()`（修正佔位符）
- **`templates/index.html`**：細化前端錯誤訊息顯示邏輯
- **新增 `test_qcom.py`**：standalone 測試腳本（需要 Flask 伺服器運行中、有效 API Key）
- **依賴**：不新增外部 lib，全用 stdlib `re` + `json` 處理修復邏輯
