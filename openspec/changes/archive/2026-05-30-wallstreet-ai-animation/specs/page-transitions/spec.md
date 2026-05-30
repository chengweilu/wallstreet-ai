## ADDED Requirements

### Requirement: Landing → Loading 淡出過渡
當使用者提交分析時，landing section SHALL 以淡出動畫退場，再切換 display。

#### Scenario: 點擊分析按鈕
- **WHEN** 使用者點擊 `.btn-analyze`
- **THEN** landing section 在 250ms 內淡出（opacity 1→0, translateY 0→-8px），動畫完成後切換 `display: none`，loading section 淡入

### Requirement: Loading → Report 淡入過渡
分析完成後，loading section SHALL 淡出，report section SHALL 淡入滑上。

#### Scenario: 分析完成
- **WHEN** API 回傳分析結果，資料渲染完畢
- **THEN** loading section 淡出（200ms），report section 從 `translateY(16px)` 滑入並淡入（400ms ease-out）

### Requirement: 返回 Landing 過渡
點擊「重新分析」時，report section SHALL 淡出，landing section SHALL 淡入回正位。

#### Scenario: 點擊重新分析按鈕
- **WHEN** 使用者點擊 `#btn-new`（重新分析）
- **THEN** report 淡出（200ms），landing 淡入（300ms），input 欄位清空並自動 focus

### Requirement: 無障礙支援
所有動畫 SHALL 在 `prefers-reduced-motion: reduce` 時被禁用，直接切換 display 不播放動畫。

#### Scenario: 使用者設定減少動畫
- **WHEN** 系統設定 `prefers-reduced-motion: reduce`
- **THEN** 所有 CSS animation / transition 時長縮為 0ms，頁面切換瞬間完成
