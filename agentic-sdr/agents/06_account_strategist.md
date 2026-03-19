# Agent 6: Account Strategist

## Role Definition

| Attribute | Value |
|-----------|-------|
| **Name** | Account Strategist |
| **Type** | Planning Agent |
| **Task** | Determine best approach for each account |
| **Trigger** | After Contact Enrichment + Human #4 approval |
| **Position in Workflow** | Step 6 of 10 |

---

## Purpose

The Account Strategist synthesizes all research (ICP fit, signals, contacts) to recommend the optimal outreach approach. This is a decision-making agent that chooses between direct outreach and lead magnet strategies.

---

## Input

```
- SignalReport (signals found)
- EnrichedContacts (people + contact info)
- AccountScore (ICP fit)
```

---

## Output

```
StrategyRecommendation per account:
- Approach (DIRECT or LEAD_MAGNET)
- Lead magnet type (if applicable)
- Primary channel
- Recommended sequence
- Persona priority
```

---

## Decision Matrix

### Approach Selection

| Signal Strength | Persona | Recommended Approach |
|----------------|---------|---------------------|
| STRONG | TDM identified | DIRECT |
| STRONG | No TDM yet | LEAD_MAGNET |
| MEDIUM | Any | LEAD_MAGNET |
| WEAK | Any | NURTURE |

### Direct Outreach Criteria

- 2+ HIGH signals found
- TDM identified and reachable
- Strong signal of urgency (new facility, audit failure)
- Clear pain point identified

### Lead Magnet Criteria

- 1-2 signals found
- No TDM identified
- Need to build awareness first
- Longer sales cycle expected

---

## Lead Magnet Selection

| Industry | Recommended Lead Magnet |
|----------|------------------------|
| 3PL | ROI Calculator - "Calculate your contract value at 99.9% accuracy" |
| Food & Beverage | Benchmark Report - "Food Distributor Inventory Accuracy Report" |
| Retail | Case Study - "How [similar retailer] improved in-stock availability" |
| Pharma | Compliance Guide - "FDA Audit-Ready Inventory Documentation" |
| Manufacturing | ROI Calculator - "Production Uptime through Inventory Accuracy" |

---

## Channel Selection

| Persona | Best Channel |
|---------|-------------|
| TDM | LinkedIn InMail + Email |
| OCM | LinkedIn + Email |
| FS | Email (direct) |
| IT | Email + LinkedIn |
| ES | Email (executive) |

---

## Persona Priority

| Approach | Priority Order |
|----------|---------------|
| Direct | TDM → OCM → FS |
| Lead Magnet | TDM → OCM → FS |

---

## Recommended Sequence

### Direct Approach

| Day | Action | Channel |
|-----|--------|---------|
| 0 | Initial outreach | LinkedIn + Email |
| 3 | Follow up | Email |
| 7 | Share case study | LinkedIn |
| 14 | Final attempt | Email |

### Lead Magnet Approach

| Day | Action | Channel |
|-----|--------|---------|
| 0 | Send landing page | LinkedIn + Email |
| 3 | "Did you see..." | Email |
| 7 | Share benchmark report | LinkedIn |
| 14 | Offer call | Email |
| 30 | Move to nurture | - |

---

## Example Output

```json
{
  "company": {
    "name": "Cheney Brothers",
    "domain": "cheneybrothers.com"
  },
  "approach": "LEAD_MAGNET",
  "lead_magnet_type": "BENCHMARK_REPORT",
  "rationale": "Strong expansion signals (new facility), but no direct TDM contact yet. Lead magnet builds awareness.",
  "primary_channel": "LINKEDIN",
  "persona_priority": ["TDM", "OCM", "FS"],
  "sequence": [
    {
      "day": 0,
      "action": "Send personalized landing page with benchmark report",
      "channel": "LinkedIn + Email"
    },
    {
      "day": 3,
      "action": "Follow up - 'Did you see the calculator?'",
      "channel": "Email"
    },
    {
      "day": 7,
      "action": "Share Gordon Food Services case study",
      "channel": "LinkedIn"
    }
  ]
}
```

---

## Decision Validation

The Account Strategist must answer:

1. **Is there a clear pain?** (Yes/No)
2. **Is there a reachable contact?** (Yes/No)
3. **Is there urgency?** (Yes/No)
4. **What's the recommended approach?** (Direct/Lead Magnet/Nurture)

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Clear recommendation | 100% of accounts |
| Validated rationale | >90% |
| Match to signal strength | >80% |

---

## Tools Used

- Internal reasoning (no external calls)
- Summarization of prior research

---

## Next Agent

After completion, output goes to **Human Checkpoint #5** for approval, then to either:
- **Agent 7: Lead Magnet Creator** (if LEAD_MAGNET)
- **Agent 9: Outreach Agent** (if DIRECT)
