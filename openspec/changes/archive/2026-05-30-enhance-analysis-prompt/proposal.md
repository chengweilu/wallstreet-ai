## Why

現有 `build_prompt()` 採單一 Claude 呼叫，輸出品質完全依賴模型訓練知識，缺乏結構化的分析框架與數據可信度機制。引入 `financial-deep-research` skill 的 8 階段研究方法論，強化 prompt 的分析深度、加入三角驗證指示與信心評分，讓報告更具機構分析師水準。

## What Changes

- 強化 `build_prompt()` 加入**分析框架指示**：要求 Claude 依序執行「範疇界定 → 假設驗證 → 三角交叉 → 合成 → 自我批判」
- 加入**數據可信度標記**：prompt 中明確告知哪些數據來自 Yahoo Finance（可信），哪些需由 AI 估算（需標示信心分）
- 加入**空頭偏誤矯正指示**：要求分析師角色對多頭論點進行自我辯論（devil's advocate），避免過度樂觀
- 新增 `confidence_score`（0–100）欄位到 JSON schema，反映報告整體數據完整度
- 在 section1–7 各加入 `data_sources` 陣列欄位，標記每個分析段落的主要依據
- 強化 Section 4 估值分析：要求同時列出 DCF、P/E、EV/EBITDA 三種方法並加權

## Capabilities

### New Capabilities
- `prompt-framework`: 在 build_prompt 中加入 financial-deep-research 8 階段框架指示
- `confidence-scoring`: JSON schema 加入 confidence_score + data_sources 欄位，後端計算數據完整度分數
- `valuation-triangulation`: Section 4 加入 EV/EBITDA 估值法與三法加權結果

### Modified Capabilities

## Impact

- 僅修改 `app.py` 中的 `build_prompt()` 函式與 `get_stock_data()` 數據品質計算
- JSON schema 新增欄位（向後兼容，前端 index.html 需加入顯示邏輯）
- 不影響 Flask 路由、DB、或前端 JS 核心邏輯
