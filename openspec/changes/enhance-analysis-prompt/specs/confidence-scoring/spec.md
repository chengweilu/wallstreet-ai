## ADDED Requirements

### Requirement: 後端計算數據完整度分數
`app.py` SHALL 在呼叫 Claude 前計算 `data_completeness_score`（0–100 整數），根據 Yahoo Finance 返回的關鍵欄位完整比例加權計算，並注入 prompt 告知 Claude。

#### Scenario: 數據齊全時
- **WHEN** `currentPrice`、`trailingPE`、`financials`、`grossMargins`、`returnOnEquity` 皆有值
- **THEN** `data_completeness_score` >= 80

#### Scenario: 數據缺失時
- **WHEN** 超過半數關鍵欄位為 None
- **THEN** `data_completeness_score` < 50，prompt 加強提示 Claude 明確標記估算欄位

### Requirement: JSON schema 加入 confidence_score 欄位
Claude 回傳的 JSON SHALL 包含頂層 `confidence_score`（整數 0–100）欄位，由 Claude 根據其估算比例自評報告整體信心程度。

#### Scenario: 報告包含 confidence_score
- **WHEN** Claude 回傳分析 JSON
- **THEN** JSON 頂層含 `"confidence_score": <整數>` 欄位

### Requirement: 前端顯示信心分數
Report Header 的 `.key-metrics` 區塊 SHALL 顯示 `confidence_score` 作為「分析信心」指標。

#### Scenario: 顯示信心分數
- **WHEN** report 渲染完成
- **THEN** metrics bar 新增一欄「分析信心」，顯示分數與顏色（≥80 綠，50–79 琥珀，<50 紅）
