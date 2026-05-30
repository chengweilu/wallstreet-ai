## ADDED Requirements

### Requirement: Report Header 暖橙漸層背景
Report Header 背景 SHALL 使用三段漸層 `linear-gradient(160deg, #1c1917 0%, #2c2420 60%, #3b1f0a 100%)`，以加入微暖橙色調替代純黑。

#### Scenario: 漸層可見
- **WHEN** 使用者看到報告標題區域
- **THEN** 背景應由深石灰向右下角呈現微暖橙色調漸層

### Requirement: 評分章圓角方形化
`.rating-stamp` 與 `.final-rating-stamp` 的 `border-radius` SHALL 分別改為 `20px` 和 `24px`，邊框厚度改為 `1.5px`，並加入 `::after` 內層光影。

#### Scenario: 評分章外觀
- **WHEN** 使用者看到報告頂部的評分章
- **THEN** 應看到圓角方形（非圓形）的評分章，帶有半透明內層光影

#### Scenario: 最終評分章外觀
- **WHEN** 使用者看到第 7 節的最終投資策略評分章
- **THEN** 應看到 140×140px 的圓角方形評分章

### Requirement: 指標列琥珀色 hover
`.metric-item` hover 狀態 SHALL 改為 `background: rgba(217,119,6,0.08)`（琥珀色微光），取代原本的純白透明度提升。

#### Scenario: 指標 hover 效果
- **WHEN** 使用者 hover 到指標列的任一格（如現價、目標價）
- **THEN** 該格背景應顯示暖琥珀色微光，而非冷白色

### Requirement: 章節序號圓角方形化
`.sec-num` SHALL 改為 `border-radius: 8px`，使用 `inline-flex` 對齊，font-family 加入 `'Inter'`。

#### Scenario: 章節序號外觀
- **WHEN** 使用者看到任一報告章節標題（如「1 商業模式與未來潛力」）
- **THEN** 章節序號應為小圓角方形數字徽章，而非圓形
