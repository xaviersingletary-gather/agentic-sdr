# Agent 2: ICP Qualifier

## Role Definition

| Attribute | Value |
|-----------|-------|
| **Name** | ICP Qualifier |
| **Type** | Scoring Agent |
| **Task** | Score accounts against ICP criteria |
| **Trigger** | After Prospector + Human #1 approval |
| **Position in Workflow** | Step 2 of 10 |

---

## Purpose

The ICP Qualifier takes the raw candidate list from the Prospector and scores each company against Gather AI's Ideal Customer Profile. It determines which accounts are worth pursuing and assigns a priority level.

---

## Input

```
List[Company] - Output from Prospector:
- Company name
- Domain
- Revenue estimate
- Facility count
- Industry
- Geography
```

---

## Output

```
List[AccountScore] - Each account scored:
- Company details
- ICP fit score (HIGH/MEDIUM/LOW)
- Score breakdown by dimension
- Reason for scoring
```

---

## Scoring Matrix

| Criteria | Weight | HIGH (3) | MEDIUM (2) | LOW (1) | OUT (0) |
|----------|--------|-----------|-------------|---------|---------|
| **Revenue** | 20% | $500M+ | $200-500M | <$200M | - |
| **Facilities** | 20% | 11+ | 5-10 | 1-4 | - |
| **Industry** | 20% | In-scope* | Adjacent | Peripheral | Out |
| **WMS** | 20% | Tier 2+ | Legacy | Unknown | None |
| **Geography** | 20% | US/Canada | - | - | Other |

*In-scope industries: Manufacturing, Food & Beverage, Retail (eCommerce, automotive, apparel), 3PL/Logistics, Integrated Healthcare/Pharma, CPG

---

## Score Calculation

```
ICP_Score = (Revenue_Score + Facilities_Score + Industry_Score + WMS_Score + Geography_Score) / 5

Where:
- HIGH = 2.5 - 3.0
- MEDIUM = 1.5 - 2.4
- LOW = 0.5 - 1.4
- OUT = 0 (any "OUT" = automatic OUT)
```

---

## Research Process

### Step 1: Validate Revenue
For each company, search for:
- Company website (about page, press releases)
- Crunchbase, ZoomInfo, LinkedIn
- News articles about funding/growth

### Step 2: Validate Facilities
Search for:
- Company press releases on expansions
- Job postings mentioning locations
- LinkedIn page for office/warehouse locations

### Step 3: Determine Industry
Confirm the company operates in an in-scope industry:
- Is it a warehouse/fulfillment 3PL?
- Is it a manufacturer with distribution?
- Is it a retailer with DCs?

### Step 4: Infer WMS
Look for signals of WMS maturity:
- Job postings for WMS roles
- Technology partnerships mentioned
- Integration capabilities

### Step 5: Assign Score
Calculate overall ICP fit and return with justification

---

## Output Fields

| Field | Description |
|-------|-------------|
| `company` | Full company object |
| `icp_fit` | HIGH, MEDIUM, LOW, or OUT |
| `revenue_score` | Score 0-3 |
| `facilities_score` | Score 0-3 |
| `industry_score` | Score 0-3 |
| `wms_score` | Score 0-3 (inferred) |
| `geography_score` | Score 0-3 |
| `reason` | Human-readable explanation |

---

## Example Output

```json
{
  "company": {
    "name": "Smart Warehousing",
    "domain": "smartwarehousing.com"
  },
  "icp_fit": "HIGH",
  "revenue_score": 3,
  "facilities_score": 3,
  "industry_score": 3,
  "wms_score": 3,
  "geography_score": 3,
  "reason": "18 facilities (well above 11 threshold), proprietary AI-powered WMS, 3PL industry, US-based"
}
```

---

## Decision Rules

| Score | Action |
|-------|--------|
| HIGH | Auto-proceed to Signal Hunter |
| MEDIUM | Flag for human review - may proceed |
| LOW | Flag for human review - unlikely to proceed |
| OUT | Auto-exclude - do not proceed |

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Accounts scored | 100% of input |
| HIGH accuracy | >80% verified |
| Processing time | <5 min per account |

---

## Tools Used

- `web_search` - Validate firmographics
- `web_fetch` - Get company details
- Internal scoring logic

---

## Next Agent

After completion, output goes to **Human Checkpoint #2** for approval, then to **Agent 3: Signal Hunter** (for HIGH scores).
