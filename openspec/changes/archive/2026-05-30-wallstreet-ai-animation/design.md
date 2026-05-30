## Context

WallStreet AI 是單一 HTML 檔案架構（index.html, 1955 行），CSS 全部在 `<style>` 區塊，JS 在底部處理資料渲染與 API 呼叫。動畫實作限定純 CSS keyframes + transition，不可引入 GSAP、Framer Motion 等新函式庫。

## Goals / Non-Goals

**Goals:**
- 所有動畫使用純 CSS（`@keyframes`, `transition`, `animation`）
- 依照 `web-animation-design` skill 的 easing 原則：進場用 `ease-out`，移動用 `ease-in-out`，hover 用 `ease`
- 動畫時長：micro-interaction 150–200ms，進場動畫 300–500ms，stagger 間距 60ms
- 支援 `@media (prefers-reduced-motion: reduce)` 全域關閉動畫
- JS 側僅新增觸發 class（`.is-visible`, `.animate-in`）不改動資料邏輯

**Non-Goals:**
- 不使用 JavaScript Animation API / Web Animations API
- 不引入任何新 npm 套件或 CDN 函式庫
- 不修改 Chart.js 圖表渲染行為
- 不變更 Flask 後端或 API 結構

## Decisions

### D1: CSS-only 動畫策略
選擇純 CSS keyframes 而非 JS 動畫函式庫。
**理由**：專案為單一 HTML 檔，無建置工具，引入新依賴成本高；CSS 動畫由瀏覽器合成層處理，效能更好。

### D2: Stagger 透過 CSS `animation-delay` 實現
Landing Hero 的標題、副標題、input card 使用 `animation-delay: 0ms / 120ms / 240ms`。
**理由**：不需要 JS 計算，瀏覽器直接執行，簡單可靠。

### D3: Intersection Observer 觸發 Report 區塊進場
Report 各 section 使用 `IntersectionObserver` 監測，進入視窗時加上 `.is-visible` class 觸發 CSS animation。
**理由**：純 CSS 無法感知滾動位置，需要最少量 JS 橋接；Observer 為瀏覽器原生 API，不需額外依賴。

### D4: Loading shimmer 使用 `background-position` 動畫
Skeleton loader 使用 `linear-gradient` + `background-size: 200%` + `animation` 移動背景位置模擬 shimmer。
**理由**：效能優，無需額外 DOM 元素，純 CSS 即可實現。

### D5: Page transition 使用 `opacity + transform` fade
Landing → Loading → Report 切換時，對容器加 `fadeOut` class，動畫結束後切換 `display`。
**理由**：`opacity` 和 `transform` 不觸發 layout reflow，為 GPU 合成層屬性，效能最佳。

## Risks / Trade-offs

- [風險] JS `display: none/flex` 切換與 CSS 動畫衝突 → 緩解：`fadeOut` 動畫結束後用 `animationend` 事件再切換 display
- [風險] Intersection Observer 在舊 Safari 不支援 → 緩解：加 `if ('IntersectionObserver' in window)` 檢查，fallback 為立即顯示
- [取捨] stagger 動畫在慢網路下可能感覺多餘 → 動畫時長控制在 500ms 內，整體流暢不過度
