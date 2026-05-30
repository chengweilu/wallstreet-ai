## Why

WallStreet AI 的現有介面功能完整，但視覺精緻度不足，Card 圓角過小、評分章以圓形呈現顯得老式、表格缺乏 zebra stripe、Landing 的 Feature 區塊佔空間過大。提升視覺層次能強化使用者對「機構級分析工具」的信任感，並改善閱讀體驗。

## What Changes

- Landing Hero 標題字體放大（clamp 上限 52px → 58px），行高從 1.15 收緊為 1.08
- Input Card 底部加入分隔線，History 按鈕融入卡片底部（移除外框感）
- Feature 區塊從 3 欄卡片格改為水平 chip 列（更輕盈不佔空間）
- Navbar active 狀態改用底線指示（移除背景色塊）
- Report Header 背景加入暖橙漸層尾段（`#1c1917 → #3b1f0a`）
- 評分章（Rating Stamp）、章節序號、History Stamp 全部從 `border-radius:50%` 改為圓角方形
- Metrics 指標列 hover 改為琥珀色微光（`rgba(217,119,6,0.08)`）
- Cards 與 Chart Cards 圓角加大（16px → 18px），陰影更柔和，加入 hover 上浮效果
- Data Table 加入 zebra stripe（偶數行 `#fafaf9`），表頭字體精緻化
- 情境卡目標價數字放大（28px → 36px），切換為 Inter 字體
- 分析按鈕加入立體 box-shadow

## Capabilities

### New Capabilities
- `ui-landing-hero`: Landing 頁面視覺結構改善，含標題、Input Card、Feature chips
- `ui-report-header`: Report Header 漸層背景與評分章圓角方形改造
- `ui-cards-tables`: Cards、Chart Cards、Data Table、Scenario Cards 的精緻化升級

### Modified Capabilities
（無現有 spec 需要修改，本次為純前端視覺變更）

## Impact

- 影響檔案：`stock_analyzer/templates/index.html`（CSS `<style>` 區段與部分 HTML 結構）
- 不影響任何 Python 後端、API 路由、JavaScript 邏輯
- 不引入新的前端依賴或框架
- 使用現有 CSS 變數系統（`--amber`, `--stone`, `--cream` 等），不破壞現有主題
