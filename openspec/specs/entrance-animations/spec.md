# entrance-animations Specification

## Purpose
TBD - created by archiving change wallstreet-ai-animation. Update Purpose after archive.
## Requirements
### Requirement: Landing Hero 進場動畫
Landing Hero 各元素 SHALL 在頁面載入時依序以 fade-in + slide-up 方式進場，stagger 間距 120ms。
順序：landing-badge (0ms) → landing-title (120ms) → landing-sub (240ms) → input-card (360ms) → features (480ms)。

#### Scenario: 標準進場
- **WHEN** 使用者載入頁面
- **THEN** landing-badge 先出現，其後每個元素依序淡入滑入，整體完成時間 ≤ 800ms

#### Scenario: 動畫結束後元素穩定
- **WHEN** 進場動畫完成
- **THEN** 所有元素保持完全可見（opacity: 1），不閃爍不消失

### Requirement: Report 區塊滾動進場
Report 內各 section（`.section-wrap`）的卡片 SHALL 在進入視窗時觸發 fade-in + slide-up 動畫。

#### Scenario: 卡片滾動進入視窗
- **WHEN** 使用者滾動頁面，卡片進入視窗 90px 以上
- **THEN** 卡片觸發進場動畫（duration: 400ms, ease-out）

#### Scenario: 已顯示卡片不重複動畫
- **WHEN** 使用者滾動後再滾回
- **THEN** 已觸發動畫的卡片保持可見，不重複播放

### Requirement: Report Header 進場
Report Header 的 `.company-info`、`.rating-stamp`、`.key-metrics` SHALL 在 report section 顯示時依序進場。

#### Scenario: Report 顯示時
- **WHEN** report section 從 `display: none` 切換為可見
- **THEN** company-info 先出現，rating-stamp 以 scale + fade 方式出現（delay 150ms），metrics 列最後滑入（delay 300ms）

