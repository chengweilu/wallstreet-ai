## 1. 修復 yfinance 重試機制（`app.py`）

- [x] 1.1 在 `get_stock_data()` 中對 `stock.info`、`stock.financials`、`stock.cashflow`、`stock.history()` 加入 `for attempt in range(3)` + `time.sleep(2 ** attempt)` 重試邏輯，捕捉 `yfinance.exceptions.YFRateLimitError`
- [x] 1.2 確認 `requests.Session` 含 `User-Agent` header 已正確傳入 `yf.Ticker(ticker, session=session)`
- [x] 1.3 三次重試後仍失敗時，設定 `result['_data_quality'] = 'limited'` 並繼續執行（不拋出例外）

## 2. 修正 Prompt 佔位符（`app.py`）

- [x] 2.1 將 `build_prompt()` 中所有 `目標價數字`、`護城河評分1到10`、`數字`、`佔比數字` 等中文佔位符改為 `<數字，如: 185.5>`、`<1-10整數>`、`<正整數>`，避免 Claude 直接將中文寫入 JSON 值
- [x] 2.2 在 JSON schema 中加入行內範例值 comment（`// 例如: 185.5`），讓 Claude 的輸出更規範

## 3. 強化 JSON 解析（`app.py`）

- [x] 3.1 提取 `repair_json(raw: str) -> dict` 函數，實作 Layer 1–4 fallback：
  - Layer 1: `json.loads(raw)` 直接解析
  - Layer 2: 正則清理後再解析（移除 trailing comma `re.sub(r',(\s*[}\]])', r'\1', raw)`、移除 `//` 行注解）
  - Layer 3: 抓 `raw[raw.find('{') : raw.rfind('}')+1]` 截斷修復
  - Layer 4: 拋出含 `raw[:300]` 的 `ValueError`
- [x] 3.2 在 `analyze()` route 將 `json.loads(raw.strip())` 替換為 `repair_json(raw)`
- [x] 3.3 `json.JSONDecodeError` except 改為捕捉 `ValueError`，錯誤訊息含 raw 輸出摘要

## 4. 建立端對端測試腳本（`test_qcom.py`）

- [x] 4.1 建立 `test_qcom.py`，讀取 `ANTHROPIC_API_KEY`（優先環境變數，次 `.env` 文件）
- [x] 4.2 加入連線檢查：`GET http://127.0.0.1:5000/`，失敗顯示啟動提示
- [x] 4.3 `POST /api/analyze` with `{"ticker": "QCOM", "api_key": KEY}`，設定 timeout=180 秒
- [x] 4.4 驗證必要欄位存在且型別正確（`moat_score` 1–10、`rating` in BUY/HOLD/AVOID 等）
- [x] 4.5 打印結構化摘要：公司名、評等、現價、12M目標價、護城河分數、財務體質、估值狀態

## 5. 執行 QCOM 測試並確認正常

- [ ] 5.1 確保 Flask 伺服器啟動（`python3 app.py`）
- [ ] 5.2 執行 `python3 test_qcom.py`，確認輸出 `✅ QCOM 分析成功`
- [ ] 5.3 打開瀏覽器 `http://localhost:5000`，手動輸入 QCOM 確認報告正常顯示（7大章節 + 圖表 + AI Sandbox 全部呈現）
