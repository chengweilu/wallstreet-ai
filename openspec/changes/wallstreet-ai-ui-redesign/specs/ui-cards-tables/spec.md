## ADDED Requirements

### Requirement: Cards 圓角與陰影升級
`.card` 與 `.chart-card` 的 `border-radius` SHALL 改為 `18px`，陰影改為 `0 1px 12px rgba(28,25,23,0.05)`，hover 時上浮 `translateY(-1px)` 並加深陰影。

#### Scenario: Card hover 效果
- **WHEN** 使用者 hover 到任一資訊卡
- **THEN** 卡片應輕微上浮（-1px）並陰影加深

#### Scenario: Chart Card hover 效果
- **WHEN** 使用者 hover 到圖表卡
- **THEN** 圖表卡應同樣顯示 hover 上浮與陰影加深

### Requirement: Card Title 精緻化
`.card-title` 字體 SHALL 改為 `11px`，letter-spacing 改為 `0.09em`，左側 amber 線條厚度改為 `2.5px`，高度 `13px`。

#### Scenario: Card Title 樣式
- **WHEN** 使用者看到任一卡片標題（如「核心商業模式」）
- **THEN** 應看到精緻的小型大寫標題，左側帶有細 amber 線條

### Requirement: Data Table zebra stripe
`.data-table` 的偶數 `tbody tr` SHALL 具備 `background: #fafaf9` 底色（zebra stripe），hover 改為 `rgba(217,119,6,0.04)`。

#### Scenario: 表格斑馬紋
- **WHEN** 使用者看到競爭對手比較表格
- **THEN** 偶數列應有輕微灰白底色，奇數列為白色

#### Scenario: 表格 row hover
- **WHEN** 使用者 hover 到表格任一列
- **THEN** 該列背景應顯示極淡琥珀色

### Requirement: Data Table 表頭精緻化
`.data-table th` 的 `font-size` SHALL 改為 `10px`，`letter-spacing` 改為 `0.08em`，`border-bottom` 改為 `1px`（移除 2px 粗線）。

#### Scenario: 表頭樣式
- **WHEN** 使用者看到比較表格的表頭列
- **THEN** 表頭文字應更小更精緻，底部邊線為細線

### Requirement: 情境卡目標價數字放大
`.sc-target` 的 `font-size` SHALL 改為 `36px`，加入 `font-family: 'Inter'`、`line-height: 1`、`letter-spacing: -0.02em`。

#### Scenario: 情境卡目標價顯示
- **WHEN** 使用者看到三大情境卡（多頭/基本/空頭）
- **THEN** 目標價數字應以 36px Inter 字體顯示，具衝擊力

### Requirement: History Stamp 圓角方形化
`.hc-stamp` 的 `border-radius` SHALL 改為 `10px`，邊框改為 `1.5px`。

#### Scenario: 歷史記錄評分章外觀
- **WHEN** 使用者查看歷史分析記錄頁面
- **THEN** 每張歷史卡片的評分章應為圓角方形，與報告頁一致

### Requirement: History Card 圓角升級
`.history-card` 的 `border-radius` SHALL 改為 `18px`，陰影改為 `0 1px 12px rgba(28,25,23,0.05)`。

#### Scenario: 歷史卡片外觀
- **WHEN** 使用者看到歷史記錄頁面的卡片
- **THEN** 卡片圓角應與報告頁的 cards 一致
