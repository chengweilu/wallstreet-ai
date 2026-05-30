## ADDED Requirements

### Requirement: 按鈕按壓回饋
`.btn-analyze` SHALL 在點擊時有明確的按壓動畫回饋（scale-down + shadow 縮小）。

#### Scenario: 點擊分析按鈕
- **WHEN** 使用者點擊 `.btn-analyze`
- **THEN** 按鈕在 150ms 內 scale 至 0.97，陰影縮小，釋放後 200ms 內回彈

### Requirement: Input Focus 動畫
`.input-wrap input` SHALL 在 focus 時有平滑的邊框顏色過渡與光暈展開動畫（非瞬間出現）。

#### Scenario: 點擊輸入框
- **WHEN** 使用者點擊 input 欄位
- **THEN** 邊框顏色在 200ms 內過渡至 amber，外圈光暈在 250ms 內展開

### Requirement: Feature Chip Hover 動畫
`.feature` chip SHALL 在 hover 時有上浮 + 邊框顏色過渡動畫。

#### Scenario: Hover feature chip
- **WHEN** 使用者 hover 任一 feature chip
- **THEN** chip 向上移動 2px（translateY(-2px)），邊框轉為 amber，過渡時間 180ms ease

### Requirement: Nav Link Active 指示動畫
`.nav-link` 底線指示器 SHALL 在切換 active 狀態時有滑動過渡而非瞬間切換。

#### Scenario: 切換 nav section
- **WHEN** 使用者滾動到不同 section
- **THEN** active 底線指示器在 200ms 內過渡到新連結

### Requirement: Metric Item Hover 微動畫
`.metric-item` SHALL 在 hover 時有背景色漸變與輕微 scale 放大。

#### Scenario: Hover 指標欄位
- **WHEN** 使用者 hover metric bar 中任一項目
- **THEN** 背景色在 150ms 內過渡至琥珀微光，字體輕微放大（scale 1.01）
