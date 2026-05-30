# valuation-triangulation Specification

## Purpose
TBD - created by archiving change enhance-analysis-prompt. Update Purpose after archive.
## Requirements
### Requirement: EV/EBITDA 估值法加入 prompt 數據
`get_stock_data()` SHALL 從 yfinance info 額外取得 `enterpriseValue` 與 `ebitda`，並在 `build_prompt()` 中注入 prompt，要求 Claude 使用三種方法（DCF、P/E、EV/EBITDA）估算目標價。

#### Scenario: EV/EBITDA 數據存在
- **WHEN** yfinance 有 `enterpriseValue` 和 `ebitda` 數據
- **THEN** prompt 中顯示 EV/EBITDA 倍數，Claude 在 section4 引用三種方法

#### Scenario: EV/EBITDA 數據缺失
- **WHEN** yfinance 返回 None
- **THEN** prompt 標記「⚠️ AI 估算」，Claude 自行估算產業合理 EV/EBITDA 倍數

### Requirement: section4 JSON 新增三法加權欄位
Claude 回傳的 `section4` SHALL 包含 `ev_ebitda_analysis`（字串）與 `weighted_target`（數字）欄位，`weighted_target` 為三種方法加權平均目標價。

#### Scenario: 三法加權目標價
- **WHEN** Claude 完成 section4 估值分析
- **THEN** `section4.weighted_target` 為數字，`section4.ev_ebitda_analysis` 為至少 100 字的分析字串

