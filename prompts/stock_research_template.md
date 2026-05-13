# Stock Research Prompt Template
## Use this exact format to research any stock

---

## HOW TO USE THIS PROMPT

1. **Copy the entire prompt below** (everything between the line markers)
2. **Replace [STOCK_SYMBOL] with the actual stock** (e.g., INFOTECH, SUNPHARMA, MARUTI)
3. **Paste into Claude or your AI research tool**
4. **Get back framework-ready data**
5. **Share the output with me** (just paste the result)
6. **I'll run it through your framework** and give you BUY/HOLD/WAIT/SKIP decision

---

## 📋 THE PROMPT (Copy everything below this line)

```
RESEARCH PROMPT: Stock Analysis for Framework Decision

Stock to research: [STOCK_SYMBOL]
Current date: [TODAY'S DATE]
Research required by: [DATE - e.g., May 15, 2026]

OBJECTIVE: Research this stock and provide data in a specific format that can be fed into an investment framework with 4 criteria: Quality, Valuation, Moat, Management.

INSTRUCTIONS:
1. Research the stock using latest available data (as of May 2026)
2. Focus on Q4 FY26 / Latest quarterly results
3. Provide ONLY the data points listed below
4. Be specific with numbers, not vague
5. Format exactly as shown

---

## DATA REQUIRED (Answer each section)

### SECTION 1: BASIC INFO
- Stock Symbol: [e.g., INFOTECH]
- Company Name: [Full name]
- Current Stock Price: ₹[exact price]
- Sector: [e.g., IT Services, Pharmaceuticals]
- Market Cap: ₹[amount in Lakhs Crore or Crores]
- Latest Quarter: [e.g., Q4 FY26]

---

### SECTION 2: QUALITY METRICS
Provide exact numbers from latest quarterly/annual results:

**Profitability:**
- Net Profit (Latest Quarter): ₹[amount] Crore
- Net Profit Growth (YoY): +[%]
- Net Profit Margin: [%]
- Is margin growing or declining? [Growing/Stable/Declining]

**Returns:**
- Return on Equity (ROE): [%] (if available)
- Return on Assets (ROA): [%] (if available)
- If not available, state: "Not disclosed in latest results"

**Asset Quality (if applicable for sector):**
- NPA Ratio (for banks): [%] (if applicable)
- Or: [Sector-specific quality metric]

**Debt:**
- Debt-to-Equity Ratio: [x] (e.g., 0.5x)
- Is debt increasing or decreasing? [Increasing/Stable/Decreasing]

**Growth:**
- Revenue Growth (3-year CAGR or Latest YoY): [%]
- Is revenue growth >10%? [Yes/No]

**Cash Generation:**
- Free Cash Flow Status: [Positive/Negative]
- FCF Trend: [Growing/Stable/Declining]

**Earnings Quality:**
- Any one-off charges, provisions, or unusual items in latest results? [Yes/No]
- If yes, explain briefly: [Details]
- Are earnings "clean" or cluttered with one-offs? [Clean/Cluttered]

---

### SECTION 3: VALUATION METRICS
Provide current valuation numbers:

**P/E Ratio:**
- Current P/E: [x] (e.g., 18.5x)
- Historical 5-year average P/E: [x] (e.g., 22-24x)
- Current vs Historical: [Current is ___% cheaper/expensive than average]

**P/B Ratio:**
- Current P/B: [x]
- Is it <2.0x? [Yes/No]

**Dividend:**
- Annual Dividend Yield: [%] (e.g., 2.8%)
- Is it >2%? [Yes/No]
- Dividend track record: [e.g., "Consistent for 20+ years" or "Irregular"]

**Analyst Targets:**
- Average analyst target price: ₹[amount]
- Implied upside/downside: [%] (e.g., +33%, -15%)
- Analyst consensus rating: [Strong Buy / Buy / Hold / Sell]

**Valuation Assessment:**
- At what price would this stock have 20% discount to fair value? ₹[estimate]
- At what price would this stock have 30% discount to fair value? ₹[estimate]
- Current stock is at: [Discount/Fair/Premium valuation]

---

### SECTION 4: BUSINESS MOAT (Competitive Advantage)
For each, answer Yes/No/Partially and explain briefly:

**Brand & Pricing Power:**
- Does company have recognized brand? [Yes/No/Partially]
- Can it raise prices without losing customers? [Yes/No]
- Brief explanation: [1 line]

**Network Effects or Scale:**
- Does company get stronger as it grows? [Yes/No]
- Or does it have scale advantage over competitors? [Yes/No]
- Brief explanation: [1 line]

**Switching Costs:**
- Do customers face friction switching to competitors? [Yes/No]
- Brief explanation: [1 line]

**Cost Advantage:**
- Is company the lowest-cost producer? [Yes/No]
- Brief explanation: [1 line]

**Other Assets (patents, licenses, etc):**
- Does company have defensible IP, licenses, or patents? [Yes/No]
- Brief explanation: [1 line]

**Moat Assessment Summary:**
- How many moats identified above? [1/2/3/4/5]
- Overall moat strength: [Weak/Moderate/Strong/Exceptional]

---

### SECTION 5: MANAGEMENT & GROWTH
Answer each:

**Management Track Record:**
- CEO/MD name: [Name]
- How long in current role? [Years]
- Has management delivered on past guidance? [Consistently/Sometimes/Rarely]
- Any major management changes recently? [Yes/No]

**Capital Allocation:**
- How does company use profits? [Dividends / Buybacks / Reinvestment / Combination]
- Is it shareholder-friendly? [Yes/No/Neutral]

**Growth Guidance:**
- What growth is management guiding for next 3-5 years? [%] (e.g., "12-15% loan growth")
- Is guidance realistic based on market conditions? [Yes/No/Uncertain]

**Recent Developments:**
- Any major recent news? [Yes/No]
- If yes, what? [Strategic acquisition / Product launch / Market expansion / Regulatory issue / etc.]
- Impact: [Positive/Negative/Neutral]

---

### SECTION 6: RISKS & RED FLAGS
Answer:

**Major Risks:**
1. [Risk #1 - e.g., "Regulatory change could impact margins"]
2. [Risk #2]
3. [Risk #3 - if any]

**Red Flags (if any):**
- Declining profitability? [Yes/No]
- Rising debt without purpose? [Yes/No]
- Asset quality deteriorating (for banks)? [Yes/No]
- Market share losses? [Yes/No]
- Execution failures on guidance? [Yes/No]

---

### SECTION 7: SUMMARY FOR FRAMEWORK
Provide a one-line verdict for each criteria:

**Quality (Step 1):**
Verdict: [PASS / MARGINAL / FAIL]
Reason: [1 line, e.g., "ROE 16%, NPA <1%, growth 12%+"]

**Valuation (Step 2):**
Verdict: [BUY SIGNAL / HOLD / WAIT / OVERVALUED]
Current discount/premium: [e.g., "31% discount" or "Premium valuation"]
Entry point needed: ₹[price] for 20-30% discount

**Moat (Step 3):**
Verdict: [Strong (75+) / Moderate (50-75) / Weak (<50)]
Moat score: [/100]
Reason: [1 line]

**Management (Step 4):**
Verdict: [STRONG / GOOD / ADEQUATE / WEAK]
Reason: [1 line]

---

## FORMAT EXAMPLE (See how it looks when filled):

```
RESEARCH OUTPUT: [STOCK_SYMBOL]

SECTION 1: BASIC INFO
- Stock Symbol: INFOTECH
- Company Name: Infosys Limited
- Current Stock Price: ₹1,850
- Sector: IT Services
- Market Cap: ₹8.5 Lakh Crore
- Latest Quarter: Q4 FY26

SECTION 2: QUALITY METRICS
Profitability:
- Net Profit (Q4 FY26): ₹5,200 Crore
- Net Profit Growth (YoY): +12%
- Net Profit Margin: 21%
- Margin trend: Stable

Returns:
- ROE: 19%
- ROA: 12%

[... and so on]
```

---

## HOW TO GET THIS DATA

**Best sources (in order):**
1. **Moneycontrol.com** - Search stock, go to "Fundamentals" tab
2. **TradingView** - Stock page, scroll to financials
3. **Company's investor relations website** - Latest earnings call, results
4. **BSEIndia.com** - Download latest annual/quarterly report PDFs
5. **Screener.in** - Stock analysis page (shows metrics clearly)

---

## WHAT TO DO WITH THE OUTPUT

Once you have the research output:

1. **Copy the entire output** (all sections)
2. **Paste it to me**
3. **I will:**
   - Run it through your 4-step framework
   - Give you a clear decision: **BUY / HOLD / WAIT / SKIP**
   - Explain reasoning
   - Tell you if it beats HDFC Bank (your current benchmark)

---

## EXAMPLE: How to Use This

**Your message to me:**
```
Hi, I want to research [STOCK] for my June ₹40k deployment.

Here's my research output:

[PASTE THE COMPLETED RESEARCH OUTPUT HERE]

Should I buy this stock?
```

**My response:**
```
Framework Analysis: [STOCK]

Quality: PASS ✅ (ROE 15%, growth >10%)
Valuation: HOLD ⚠️ (12% discount, below 20% threshold)
Moat: 85/100 ✅ (Strong brand, switching costs)
Management: STRONG ✅ (Proven track record)

VERDICT: HOLD/WAIT
Reason: Stock is good quality but not at entry price yet.
Entry point: Buy at ₹[price] for 20% discount.

Recommendation: [Skip for now / Buy / Wait for lower price]
```

---

## TIME TO COMPLETE RESEARCH

- **For experienced investors:** 30-45 minutes per stock
- **For beginners:** 60-90 minutes per stock
- **Using screener tools:** 20-30 minutes (faster)

---

## TIPS FOR BETTER RESEARCH

1. **Focus on numbers, not narratives**
   - ❌ "Company is growing" (vague)
   - ✅ "Revenue CAGR 15%, ROE 16%" (specific)

2. **Use latest data**
   - Most recent quarter/annual results
   - Latest analyst reports
   - Current stock price

3. **Be honest about unknowns**
   - If data not available, say "Not disclosed"
   - Don't guess or estimate for major metrics

4. **Cross-check numbers**
   - If Moneycontrol says P/E 18.5x, verify on TradingView
   - Numbers should match across sources

5. **Focus on the format**
   - Stick to the sections provided
   - Don't add extra commentary
   - Keep it clean and organized

---

## READY TO RESEARCH?

**Next time you want to evaluate a stock:**

1. Copy this prompt
2. Fill in [STOCK_SYMBOL]
3. Research the company using the format
4. Send me the output
5. Get framework decision in minutes

This ensures:
✅ Consistent format across all research
✅ I can quickly apply your framework
✅ Fast decision-making
✅ No ambiguity or missing data

---

## QUICK REFERENCE: Framework Criteria Thresholds

**For framework to say BUY:**
- Quality: Must PASS (4+ of 6 metrics)
- Valuation: Must be 20-30% DISCOUNT to fair value
- Moat: Must be 75+ (Strong)
- Management: Must be STRONG or GOOD

**If ANY criteria fails:** SKIP or WAIT

---

**Save this prompt. Use it every time you research a stock.**

**It will make your investing faster, more systematic, and more profitable.** 💪
```

---

## END OF PROMPT TEMPLATE

---

## HOW TO USE IT RIGHT NOW

### Example: Research Sunpharma for June Deployment

**Your research message to me would look like:**

```
Stock Research: SUNPHARMA

SECTION 1: BASIC INFO
- Stock Symbol: SUNPHARMA
- Company Name: Sun Pharmaceutical Industries
- Current Stock Price: ₹1,450 (as of May 13, 2026)
- Sector: Pharmaceuticals
- Market Cap: ₹2.1 Lakh Crore
- Latest Quarter: Q4 FY26

SECTION 2: QUALITY METRICS
Profitability:
- Net Profit (Q4 FY26): ₹1,800 Crore
- Net Profit Growth (YoY): +18%
- Net Profit Margin: 12%
- Margin trend: Growing

[... and so on through all sections]

SECTION 7: SUMMARY FOR FRAMEWORK
Quality: PASS (ROE 15%, growth 15%+)
Valuation: 18% discount (below 20% threshold)
Moat: 70/100 (Moderate - generic pharma competition)
Management: GOOD (Consistent execution)
```

**Then I would respond:**

```
Framework Analysis: SUNPHARMA

Quality: ✅ PASS
Valuation: ⚠️ HOLD (18% discount < 20% target)
Moat: 70/100 (Moderate)
Management: GOOD

VERDICT: WAIT
Reason: Quality is good but valuation not yet at entry point.
Entry needed at ₹1,300 (20% discount).

Recommendation: SKIP for now, wait for ₹1,300 entry.
Benchmark: Still below HDFC Bank (31% discount).
```

---