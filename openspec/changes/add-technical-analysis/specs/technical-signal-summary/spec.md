## ADDED Requirements

### Requirement: 技術信號綜合評分
後端 SHALL 計算 `signal_score`（0–100）：價格>MA200(+25)、MA50>MA200(+20)、價格>MA50(+15)、RSI在40–70(+20)、MACD>Signal(+20)。

#### Scenario: 強多信號
- **WHEN** 五個條件全部滿足
- **THEN** `signal_score = 100`，`signal_label = "強烈多頭"`

#### Scenario: 強空信號
- **WHEN** 五個條件全部不滿足
- **THEN** `signal_score = 0`，`signal_label = "強烈空頭"`

#### Scenario: RSI 超買超賣不加分
- **WHEN** RSI > 70 或 RSI < 30
- **THEN** RSI 健康區間條件為 false，不加 20 分（視為過熱或過冷）

### Requirement: 信號摘要卡片
前端 SHALL 在 Section 8 頂部顯示「技術面評分」大字卡，包含 signal_score 數字、signal_label 文字、五個條件的 ✅/❌ 逐項列示。

#### Scenario: 信號卡顯示
- **WHEN** 技術分析 API 成功回傳
- **THEN** 頂部大卡顯示總分（字體與 moat_score 同樣大小）與五條件 checklist
