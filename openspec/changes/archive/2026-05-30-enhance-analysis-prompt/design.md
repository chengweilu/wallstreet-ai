## Context

`build_prompt()` 在 `app.py` 第 333 行，產生 ~200 行的 f-string prompt，直接傳給 Claude API。目前已有 Yahoo Finance 數據注入（股價、財報、毛利率等），但 Claude 被要求「依訓練知識補充」時缺乏結構化指引，容易產生過度樂觀的報告。

## Goals / Non-Goals

**Goals:**
- 在 prompt 前段加入「研究員角色框架」：三階段驗證指示（陳述假設 → 反向質疑 → 加權結論）
- 計算 `data_completeness_score`（0–100）：已有 Yahoo Finance 實際數據的欄位比例
- JSON schema 新增 `confidence_score`、`data_sources` 欄位
- Section 4 加入 `ev_ebitda` 欄位與三法加權目標價 `weighted_target`

**Non-Goals:**
- 不呼叫外部 web search API（不引入新的網路依賴）
- 不拆分成多個 Claude API 呼叫（成本控制）
- 不修改前端 chart 渲染邏輯

## Decisions

### D1: 框架指示放在 prompt 最前段
在現有 `name_lock` 之前插入角色框架，確保 Claude 在看到數據前先建立分析思維。

### D2: data_completeness_score 在後端計算
根據 `get_stock_data()` 返回的 dict，計算非 None 欄位比例（關鍵欄位加權），不依賴 Claude 自評。

### D3: EV/EBITDA 加入 prompt 數據輸入
從 yfinance `info` 取 `enterpriseValue` 和 `ebitda`，已有但未傳入 prompt，補充進去即可。

### D4: data_sources 欄位為字串陣列
格式：`["yahoo_finance_verified", "ai_estimated"]`，Claude 在每段分析標記。

## Risks / Trade-offs

- [風險] prompt 變長導致 token 成本增加 → 估計增加 ~300 tokens，可接受
- [取捨] Claude 自我標記 data_sources 準確性難以驗證 → 僅作為參考指標，不作為功能保證
