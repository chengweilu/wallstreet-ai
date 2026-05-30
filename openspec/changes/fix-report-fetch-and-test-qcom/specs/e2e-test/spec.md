## ADDED Requirements

### Requirement: Standalone test script
`test_qcom.py` 必須能在不修改任何現有程式碼的情況下單獨執行，驗證完整流程。

#### Scenario: Flask 伺服器未啟動
- **WHEN** 執行 `python3 test_qcom.py` 但 localhost:5000 無回應
- **THEN** 顯示 `❌ 無法連線到 http://localhost:5000，請先執行 python3 app.py` 並退出

#### Scenario: 缺少 API Key
- **WHEN** 環境變數 `ANTHROPIC_API_KEY` 未設定且 `.env` 中也無此值
- **THEN** 顯示 `❌ 請設定 ANTHROPIC_API_KEY` 並退出

#### Scenario: QCOM 分析成功
- **WHEN** Flask 正常運行，API Key 有效，QCOM 分析完成
- **THEN** 腳本驗證 JSON 包含以下必要欄位並打印摘要：
  - `company_name`、`ticker`（== "QCOM"）
  - `section1.core_model`（非空字串）
  - `section2.moat_score`（1–10 之間的數字）
  - `section3.health_verdict`（STRONG / WEAKENING / CONCERNING 之一）
  - `section4.valuation_verdict`
  - `section7.rating`（BUY / HOLD / AVOID 之一）
  - `sandbox`（含 scenario1/2/3）
  - 最後顯示 `✅ QCOM 分析成功！評等: BUY/HOLD/AVOID，目標價: $XXX`

#### Scenario: JSON 結構不完整
- **WHEN** 回傳 JSON 缺少必要欄位
- **THEN** 顯示具體缺少哪些欄位，顯示 `❌ JSON 結構驗證失敗` 並退出 code 1
