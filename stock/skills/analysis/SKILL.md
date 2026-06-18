---
name: stock-analysis
description: >
  Use this skill whenever the user wants to analyze a US stock, evaluate whether to buy/hold/sell,
  research a company's fundamentals, or make an investment decision. Triggers include: any mention
  of a stock ticker (e.g. AVGO, NVDA, AAPL), phrases like "分析这只股票", "should I buy X", "X股票怎么样",
  "research X for me", "给我看看X的分析", or any request to evaluate a publicly traded company.
  Also trigger when the user mentions entry price, position sizing, or asks about valuation.
  This skill produces a structured Buy/Hold/Sell analysis report with fundamentals, valuation,
  technicals, and risk factors.
---

# Stock Analysis Skill

Produces a structured investment analysis report for a US-listed stock, given a ticker symbol.
Uses IBKR MCP for real-time price data and web search for fundamentals, news, and analyst views.

---

## Step 1: Gather Data

Use **both** sources in parallel where possible:

### IBKR MCP
- `search_contracts` — confirm the ticker and get the contract ID
- `get_price_snapshot` — current price, 52-week high/low, volume
- `get_price_history` — 3–6 month daily OHLCV for technical read
- `get_company_connections` — competitors and sector exposure
- `get_company_themes` — industry/trend classification

### Web Search
Search for the following and synthesize (do not copy verbatim):
1. `{TICKER} revenue earnings growth 2024 2025` — recent financials
2. `{TICKER} PE ratio valuation analyst target price` — valuation multiples
3. `{TICKER} risks headwinds bear case` — risk factors
4. `{TICKER} latest news earnings guidance` — recent catalysts

---

## Step 2: Build the Report

Output a structured markdown report with these exact sections:

---

### 📊 {COMPANY NAME} ({TICKER}) — Investment Analysis

**Current Price:** $X.XX　｜　**Date:** YYYY-MM-DD　｜　**Sector:** XXX

---

#### 1. 公司概况 (Company Overview)
- Business model in 2–3 sentences
- Key revenue segments and their mix (%)
- Geographic exposure

#### 2. 基本面分析 (Fundamentals)

| 指标 | 数值 | 备注 |
|------|------|------|
| 营收 (TTM) | $XXB | YoY +XX% |
| 净利润率 | XX% | vs 行业均值 |
| EPS (TTM) | $X.XX | |
| 自由现金流 | $XXB | |
| 净资产收益率 ROE | XX% | |
| 负债率 | XX% | |

- Revenue trend narrative (accelerating / decelerating / stable)
- Key growth drivers

#### 3. 估值分析 (Valuation)

| 估值指标 | 当前值 | 5年均值 | 行业均值 | 判断 |
|----------|--------|---------|---------|------|
| P/E | X | X | X | 高估/合理/低估 |
| Forward P/E | X | — | X | |
| PEG | X | — | <1 为低估 | |
| P/S | X | X | X | |
| EV/EBITDA | X | X | X | |

- DCF感性判断（若分析师目标价可得，与当前价比较）
- 分析师共识目标价 vs 当前价，隐含涨跌幅

#### 4. 技术面简析 (Technical Summary)
- 当前价格 vs 关键均线（50日/200日）
- 近期趋势（上升/下降/横盘）
- 支撑位 / 阻力位
- RSI / MACD 简要读数（若可得）

#### 5. 风险因素 (Risk Factors)
列出3–5条主要风险，每条一句话说明影响。

- ⚠️ 风险1
- ⚠️ 风险2
- ⚠️ 风险3

#### 6. 投资结论 (Verdict)

> **建议：🟢 买入 / 🟡 持有 / 🔴 卖出 / ⚪ 观望**

| | 说明 |
|--|------|
| **核心逻辑** | 1–2句核心买入/卖出理由 |
| **目标价区间** | $XX – $XX（基于估值） |
| **建议买入区间** | $XX – $XX（若建议买入） |
| **止损参考** | $XX（跌破此位需重新评估） |
| **持仓建议** | 轻仓试探 / 标准仓位 / 暂不介入 |

> ⚠️ 免责声明：以上分析仅供参考，不构成投资建议。投资有风险，决策需谨慎。

---

## Step 3: Formatting Rules

- Use markdown tables for all structured data
- Use emoji indicators: 🟢 positive / 🟡 neutral / 🔴 negative / ⚠️ risk
- All currency in USD unless noted
- If data is unavailable, mark as `N/A` — never fabricate numbers
- Keep each section concise; total report ~600–900 words
- End with the disclaimer

---

## Data Availability Notes

- IBKR MCP provides real-time price and historical OHLCV; use it for all price/technical data
- Fundamentals (revenue, EPS, margins) come from web search — prefer sources like Macrotrends, Wisesheets, or earnings releases
- If IBKR data is unavailable, fall back entirely to web search
- Always state data source uncertainty where relevant (e.g., "based on TTM estimates")
