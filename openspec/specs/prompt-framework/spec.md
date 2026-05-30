# prompt-framework Specification

## Purpose
TBD - created by archiving change enhance-analysis-prompt. Update Purpose after archive.
## Requirements
### Requirement: 分析師角色框架指示
`build_prompt()` 的 prompt 開頭 SHALL 包含三階段分析框架指示，要求 Claude 在生成報告前先執行：1) 陳述數據來源可信度，2) 對多頭論點進行魔鬼代言人質疑，3) 給出加權後的最終判斷。

#### Scenario: 框架指示出現在 prompt 前段
- **WHEN** `build_prompt()` 生成 prompt
- **THEN** prompt 在 `name_lock` 之前包含「三階段研究框架」段落

#### Scenario: 框架要求 devil's advocate
- **WHEN** Claude 執行分析
- **THEN** section5 的 bear_point 質量更高，包含具體數據反駁而非泛泛風險

### Requirement: 數據來源透明標記
Prompt SHALL 明確告知 Claude 哪些數據為 Yahoo Finance 實際值（高可信），哪些為空值需估算，讓 Claude 生成時能區分標記。

#### Scenario: 有 Yahoo Finance 數據
- **WHEN** `currentPrice`、`trailingPE` 等欄位有值
- **THEN** prompt 中以「✅ 已驗證」標記這些數字

#### Scenario: 無數據需估算
- **WHEN** 某欄位為 None 或 0
- **THEN** prompt 中以「⚠️ AI 估算」標記，要求 Claude 明確說明估算依據

