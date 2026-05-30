## ADDED Requirements

### Requirement: API 回傳資料來源物件
後端 `POST /api/analyze` 的回傳 `data` 物件 SHALL 包含 `data_sources` 欄位，標明每個關鍵數據點的來源。

#### Scenario: 完整 yfinance 數據
- **WHEN** yfinance 成功抓取股票數據（`_data_quality == 'full'`）
- **THEN** `data_sources.current_price == "yahoo_finance"`，`data_sources.annual_data == "yahoo_finance"`

#### Scenario: yfinance 失敗使用範例數據
- **WHEN** yfinance 財務數據為空，`build_annual_data_template` 使用硬編碼範例
- **THEN** `data_sources.annual_data == "example_fallback"`

#### Scenario: AI 估算欄位標示
- **WHEN** 任何分析請求完成
- **THEN** `data_sources.target_price_12m == "claude_ai"`，`data_sources.overall_rating == "claude_ai"`，`data_sources.moat_score == "claude_ai"`

### Requirement: 前端顯示來源徽章
報告頁面 SHALL 在以下關鍵數字旁顯示來源徽章：當前股價、12M 目標價、財務表格、護城河評分。

#### Scenario: Yahoo Finance 來源徽章
- **WHEN** `data_sources.current_price == "yahoo_finance"`
- **THEN** 股價旁顯示綠色徽章「YF」

#### Scenario: AI 估算來源徽章
- **WHEN** `data_sources.target_price_12m == "claude_ai"`
- **THEN** 目標價旁顯示藍色徽章「AI」

#### Scenario: 範例數據警告徽章
- **WHEN** `data_sources.annual_data == "example_fallback"`
- **THEN** 財務表格標題旁顯示橘色徽章「⚠ 範例數據」

### Requirement: 報告底部顯示資料品質摘要卡片
報告 SHALL 在 section7 之後、AI Sandbox 之前顯示「資料品質摘要」卡片。

#### Scenario: 摘要卡片顯示來源分類
- **WHEN** 報告載入完成
- **THEN** 卡片顯示「真實市場數據」與「AI 估算」兩欄，列出各自包含的欄位

#### Scenario: 摘要卡片顯示範例數據警告
- **WHEN** `data_sources.annual_data == "example_fallback"`
- **THEN** 卡片以橘色區塊顯示「⚠ 部分財務數據為範例預設值，非真實財報」
