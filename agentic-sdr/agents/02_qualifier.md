# Agent 2: Qualifier

**Version:** 2.0  
**Role:** Score and rank accounts based on ICP fit + signal strength  
**Model Tier:** Best Reasoning (GPT-4o, Claude 3.5)  
**Frequency:** Weekly (Tuesday)

---

## Inputs

- 50 companies from Researcher
- Signal data for each company

---

## Outputs

```json
{
  "ranked_accounts": [
    {
      "company_name": "string",
      "icp_fit": "HIGH | MEDIUM | LOW",
      "signal_strength": "HOT | WARM | COLD",
      "priority_score": number (0-12),
      "score_breakdown": {
        "revenue": number,
        "facilities": number,
        "industry": number,
        "signals": number,
        "recency": number
      },
      "reason": "string"
    }
  ],
  "recommended_approval": number (top 10-15)
}
```

---

## Scoring Matrix

### Firmographic Score

| Criteria | Points | Notes |
|----------|--------|-------|
| Revenue $500M+ | 3 | |
| Revenue $200-500M | 2 | |
| Revenue <$200M | 0 | **OUT - skip** |
| 11+ facilities | 3 | |
| 5-10 facilities | 2 | |
| 1-4 facilities | 0 | **OUT - skip** |
| In-scope industry | 2 | 3PL/F&B/Retail/Pharma/Mfg/CPG |
| Adjacent industry | 1 | |
| Out of scope | 0 | |

### Signal Scoring (with recency multiplier)

| Signal Age | Points |
|------------|--------|
| Within 30 days | +3 |
| Within 60 days | +2 |
| Within 90 days | +1 |
| 90+ days old | +0 (ignore) |

### Classification

| Total Score | Classification |
|-------------|---------------|
| 8-12 | **HOT** - Prioritize |
| 5-7 | WARM |
| 0-4 | COLD - Skip |

---

## Rules

1. **HARD REJECT**: Revenue <$200M OR facilities <5 OR out of scope industry
2. **ONLY** return HOT accounts for human review
3. If no HOT accounts found, return top 5 WARM with explanation
4. Include recency date for each signal in output

---

## Deduplication Check

- Check `companies` table
- If company has status="human_review_pending" OR "approved": **SKIP**

---

## Database Write

Update `companies` table:

| Field | Value |
|-------|-------|
| score | Calculated priority score |
| classification | HOT/WARM/COLD |
| status | "human_review_pending" (if HOT) or "rejected" (if COLD) |

---

## Success Criteria

- All 50 companies scored
- Clear reasoning for each score
- Return only HOT accounts for human review
