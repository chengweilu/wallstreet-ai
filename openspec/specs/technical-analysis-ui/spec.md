# technical-analysis-ui Specification

## Purpose
TBD - created by archiving change add-technical-analysis. Update Purpose after archive.
## Requirements
### Requirement: 技術面 Section 顯示
前端 HTML SHALL 在 Section 7（投資策略）之後新增 Section 8「技術面分析」，包含均線狀態、RSI 信號、MACD 方向三個資訊卡，以及一個均線疊加折線圖。

#### Scenario: 技術分析載入成功
- **WHEN** `fetchTechnicalAnalysis()` 回傳成功
- **THEN** Section 8 顯示 MA/RSI/MACD 數值與信號燈（綠/琥珀/紅），圖表渲染 90 天收盤價 + MA20/MA50/MA200 折線

#### Scenario: 技術分析載入中
- **WHEN** API 尚未回應
- **THEN** Section 8 顯示 skeleton loading 動畫（使用現有 `.skeleton-line` class）

#### Scenario: 技術分析失敗
- **WHEN** API 回傳 `success: false`
- **THEN** Section 8 顯示「技術數據暫時無法取得」提示，不影響主報告顯示

### Requirement: 均線疊加圖
均線疊加圖 SHALL 使用 Chart.js 折線圖，顯示：收盤價（白/淺色）、MA20（琥珀）、MA50（綠）、MA200（紅），Y 軸為價格，X 軸為日期。

#### Scenario: 圖表渲染
- **WHEN** `price_with_ma` 數據長度 >= 20
- **THEN** Chart.js 渲染 `.chart-card` 內的 canvas，顯示多條折線

