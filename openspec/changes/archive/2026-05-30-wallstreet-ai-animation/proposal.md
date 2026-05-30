## Why

WallStreet AI 的 UI 視覺改善已完成（wallstreet-ai-ui-redesign），但頁面目前缺乏動態感——所有元素靜態呈現，互動回饋薄弱，與「機構級分析工具」的定位不符。加入有目的性的動畫與過渡效果，能大幅提升精緻度與使用信心。

## What Changes

- 新增 Landing Hero 進場動畫：標題、副標題、input card 依序淡入滑入
- 新增 Loading 畫面升級：骨架屏效果取代單純旋轉圓圈，顯示分析進度感
- 新增 Report 進場動畫：報告 header、metrics 列、各 section 卡片依序滾入出現
- 新增微互動（Microinteractions）：按鈕按壓回饋、input focus 動畫、nav link hover
- 新增 Page Transition：從 landing → loading → report 的平滑區段切換
- 加入 `prefers-reduced-motion` 無障礙支援，尊重使用者系統偏好
- 所有動畫使用純 CSS keyframes + transition，不引入任何新框架

## Capabilities

### New Capabilities
- `entrance-animations`: Landing Hero 與 Report 各區塊的進場動畫（fade-in + slide-up）
- `microinteractions`: 按鈕、input、nav、feature chip 的互動回饋動畫
- `loading-enhancement`: Loading 畫面升級，加入 shimmer 骨架動畫與進度條平滑過渡
- `page-transitions`: Landing → Loading → Report 區段切換的淡出淡入過渡

### Modified Capabilities
<!-- 無現有 spec 需修改 -->

## Impact

- 僅修改 `/templates/index.html` 內的 CSS `<style>` 區塊與少量 JS 動畫觸發邏輯
- 不影響任何 API 呼叫、資料渲染、Chart.js 圖表、Flask 後端
- 新增約 80-120 行 CSS，新增 `@keyframes` 定義與 `.animate-in` class 工具
