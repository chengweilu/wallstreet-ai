## 1. CSS 基礎動畫工具建立

- [x] 1.1 在 `<style>` 區塊新增 `@keyframes fadeInUp`：`from {opacity:0; transform:translateY(16px)} to {opacity:1; transform:translateY(0)}`
- [x] 1.2 新增 `@keyframes fadeIn`：`from {opacity:0} to {opacity:1}`
- [x] 1.3 新增 `@keyframes scaleIn`：`from {opacity:0; transform:scale(0.92)} to {opacity:1; transform:scale(1)}`
- [x] 1.4 新增 `@keyframes shimmer`：`from {background-position:200% center} to {background-position:-200% center}`
- [x] 1.5 新增 `@keyframes pulse-scale`：`0%,100% {transform:scale(1)} 50% {transform:scale(1.02)}`
- [x] 1.6 新增 `@media (prefers-reduced-motion: reduce)` 區塊，將所有 `animation-duration` 與 `transition-duration` 設為 `0.01ms`

## 2. Landing Hero 進場動畫

- [x] 2.1 設定 `.landing-badge` 初始態：`opacity:0`，加 `animation: fadeInUp 400ms cubic-bezier(0.215,0.61,0.355,1) 0ms forwards`
- [x] 2.2 設定 `.landing-title` 加 `animation: fadeInUp 400ms cubic-bezier(0.215,0.61,0.355,1) 120ms forwards`，初始 `opacity:0`
- [x] 2.3 設定 `.landing-sub` 加 `animation: fadeInUp 400ms cubic-bezier(0.215,0.61,0.355,1) 240ms forwards`，初始 `opacity:0`
- [x] 2.4 設定 `.input-card` 加 `animation: fadeInUp 400ms cubic-bezier(0.215,0.61,0.355,1) 360ms forwards`，初始 `opacity:0`
- [x] 2.5 設定 `.features` 加 `animation: fadeIn 350ms ease 480ms forwards`，初始 `opacity:0`

## 3. 微互動（Microinteractions）

- [x] 3.1 更新 `.btn-analyze:active` CSS：加入 `transform:scale(0.97)` 與縮小陰影
- [x] 3.2 更新 `.input-wrap input` `transition`：改為 `border-color 200ms ease, box-shadow 250ms ease`
- [x] 3.3 更新 `.feature` `transition`：改為 `border-color 180ms ease, box-shadow 180ms ease, transform 180ms ease`
- [x] 3.4 更新 `.feature:hover`：加入 `transform:translateY(-2px)`
- [x] 3.5 更新 `.metric-item` CSS：加入 `transition: background 150ms ease, transform 150ms ease`
- [x] 3.6 更新 `.metric-item:hover`：加入 `transform:scale(1.01)`

## 4. Loading 畫面升級

- [x] 4.1 更新 `.loader-ring` CSS：加入 `animation: spin 0.9s linear infinite, pulse-scale 2s ease-in-out infinite alternate`
- [x] 4.2 更新 `.loader-bar` CSS：`transition` 改為 `width 0.6s cubic-bezier(0.25,0.46,0.45,0.94)`
- [x] 4.3 在 `#loading` 區塊新增 `.skeleton-line` CSS：`height:12px; border-radius:6px; background:linear-gradient(90deg, var(--stone-6) 25%, #f0eeea 50%, var(--stone-6) 75%); background-size:200% auto; animation:shimmer 1.5s linear infinite`
- [x] 4.4 在 HTML loading section 的 `.loader-sub` 後加入 2–3 個 `<div class="skeleton-line">` 占位元素

## 5. Page Transitions

- [x] 5.1 新增 `.section-fade-out` CSS class：`animation: fadeOut 250ms cubic-bezier(0.55,0,1,0.45) forwards`，並新增 `@keyframes fadeOut`：`to {opacity:0; transform:translateY(-8px)}`
- [x] 5.2 新增 `.section-fade-in` CSS class：`animation: fadeInUp 400ms cubic-bezier(0.215,0.61,0.355,1) forwards`
- [x] 5.3 找到 JS 中顯示 loading（`landing.style.display='none'` 或類似）的程式碼，改為：先加 `.section-fade-out` class，監聽 `animationend` 後再切換 `display`
- [x] 5.4 找到 JS 中顯示 report（`report.style.display=...`）的程式碼，改為：report display 設為可見後立即加 `.section-fade-in` class
- [x] 5.5 找到 JS 中「返回 Landing」邏輯（`#btn-new` 點擊），改為：report 先 `.section-fade-out`，animationend 後切換回 landing 並加 `.section-fade-in`

## 6. Report 區塊滾動進場

- [x] 6.1 新增 `.animate-card` CSS class：初始 `opacity:0; transform:translateY(20px)`
- [x] 6.2 新增 `.animate-card.is-visible` CSS：`animation: fadeInUp 400ms cubic-bezier(0.215,0.61,0.355,1) forwards`
- [x] 6.3 在 JS 底部新增 `initScrollAnimations()` 函式：使用 `IntersectionObserver`（threshold: 0, rootMargin: '0px 0px -90px 0px'），觀測 `.card, .chart-card` 元素，進入視窗時加 `.is-visible` class
- [x] 6.4 在報告渲染完成後呼叫 `initScrollAnimations()`，並對 `.card, .chart-card` 批量加上 `.animate-card` class（stagger delay 用 CSS `--i` 變數，每張卡 `animation-delay: calc(var(--i, 0) * 60ms)`）

## 7. 視覺驗證

- [x] 7.1 在瀏覽器開啟 `http://127.0.0.1:5001`，確認 Landing Hero 五個元素依序淡入滑入
- [x] 7.2 點擊 `.btn-analyze` 確認按壓 scale 回饋，hover 上浮動畫正常
- [x] 7.3 確認 landing → loading → report 的淡出/淡入過渡平滑無閃爍
- [x] 7.4 確認 report 各卡片在滾動時依序進場
- [x] 7.5 確認 loading 骨架 shimmer 動畫正常顯示
- [x] 7.6 在 System Settings 開啟「減少動態效果」，確認所有動畫關閉、頁面正常運作
