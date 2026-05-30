## Context

WallStreet AI 的前端為單一 `index.html`（約 1938 行），內含行內 `<style>` CSS、HTML 結構、Chart.js 圖表與 JavaScript 邏輯。現有設計使用 CSS 變數系統（`--amber`, `--stone`, `--cream`），視覺一致性良好，但圓角、陰影、表格、Landing 區塊的精緻度有提升空間。所有變更限定於該單一檔案。

## Goals / Non-Goals

**Goals:**
- 提升視覺精緻度與現代感，強化「機構級分析工具」的品牌信任感
- 改善資訊層次：更大的標題、更清晰的 hover 狀態、更易讀的表格
- 所有變更向後相容，不破壞現有 CSS 變數與 JS 功能

**Non-Goals:**
- 不引入 Tailwind、Bootstrap 等新框架
- 不改動任何 Python 後端或 API 邏輯
- 不重構 JavaScript（圖表、歷史記錄、滾動觀察器等）
- 不改動字體引入來源（維持 Noto Sans TC + Inter）

## Decisions

### D1：CSS 修改策略 — 就地修改現有規則，不追加覆蓋層
**決策**：直接編輯 `<style>` 區段內的現有 CSS 規則，而非在尾部追加覆蓋樣式。

**理由**：追加覆蓋會增加特異性混亂，長期難以維護。直接修改原始規則更清晰，且本次變更皆為精確的屬性替換（如 `border-radius`、`box-shadow`、`font-size`）。

**排除方案**：尾部追加覆蓋層 — 雖然風險較低，但會造成重複宣告。

### D2：評分章形狀 — 圓形改圓角方形（20px）
**決策**：`.rating-stamp`、`.final-rating-stamp`、`.hc-stamp` 全部從 `border-radius:50%` 改為圓角方形。

**理由**：圓形評分章在現代設計語境中顯得老式；圓角方形（Rounded Rectangle）更符合當前金融科技 UI 趨勢（參考 Bloomberg、Robinhood），且與 card 的圓角語言一致。

### D3：Landing Feature 區塊 — 卡片格改 chip 列
**決策**：CSS 從 `grid` 改 `flex wrap`，HTML 保留 `.feature` 元素但移除描述文字（`display:none`）。

**理由**：原 3 欄卡片格在 Landing Hero 佔用過多垂直空間，分散焦點。Chip 列更輕盈，讓使用者目光更快聚焦在輸入框。

### D4：Input Card 結構 — 加入分隔線
**決策**：在 `.input-row` 與 `.btn-history-landing` 之間新增 `.input-divider` div，CSS 定義為 `border-top: 1px solid var(--stone-6)`。History 按鈕改為融入卡片底部（移除外框 border）。

**理由**：讓主要操作（輸入 + 分析）與次要操作（查看歷史）有明確視覺分隔，同時避免兩個相互競爭的 border 產生視覺噪音。

## Risks / Trade-offs

- **[風險] CSS 特異性衝突** → 所有修改均針對已存在的 class，不新增 ID 選擇器，風險極低
- **[風險] 評分章尺寸因形狀改變看起來不同** → 寬高維持不變（120×120px），僅改 border-radius，視覺面積相同
- **[風險] Feature chip 列在極窄螢幕換行過多** → 已加入 `flex-wrap`，自然換行，不會截斷
- **[Trade-off] 描述文字 `display:none`** → 損失部分說明文字的 SEO 價值，但 Landing 本為動態應用入口，影響極微
