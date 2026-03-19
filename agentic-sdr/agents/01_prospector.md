# Agent 1: Prospector

## Role Definition

| Attribute | Value |
|-----------|-------|
| **Name** | Prospector |
| **Type** | Research Agent |
| **Task** | Find new companies matching ICP criteria |
| **Trigger** | Scheduled (weekly) or on-demand |
| **Position in Workflow** | Step 1 of 10 |

---

## Purpose

The Prospector is the first agent in the outbound sequence. Its sole job is to find *new* companies that match Gather AI's Ideal Customer Profile (ICP) but are NOT in the existing customer, target, or strategic account lists.

---

## Input

```
- ICP criteria (revenue, facilities, industry, geography)
- Exclusion list (existing customers, targets, strategic accounts)
- Source lists (ZoomInfo, Crunchbase, trade press)
```

---

## Output

```
List[Company] - Raw list of candidate companies with:
- Company name
- Domain
- Revenue (estimated)
- Facility count (estimated)
- Industry
- Geography
```

---

## Process

### Step 1: Load ICP Criteria
Load from MEMORY.md or provided ICP definition:
- Revenue: $500M+
- Facilities: 11+
- Industry: Manufacturing, Food & Bev, Retail, 3PL, Pharma, CPG
- Geography: US/Canada HQ

### Step 2: Load Exclusion List
Load existing accounts from:
- Customers (from provided list)
- Target Accounts (152 accounts)
- Strategic Accounts (13 accounts)

### Step 3: Source Candidates
Search for companies matching ICP using:
- Trade press lists (DC Velocity, Supply Chain Dive)
- Public lists (Fulfill.com top 3PLs, etc.)
- News for new companies entering the space

### Step 4: Filter & Deduplicate
- Remove companies in exclusion list
- Remove duplicates
- Keep companies meeting minimum ICP criteria

### Step 5: Return Candidate List
Output list with basic firmographics for human review

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Candidates found per run | 20-100 |
|ICP match rate | >80% |
| Duplicate rate | <5% |

---

## Tools Used

- `web_search` - Search for companies
- `web_fetch` - Get company details
- `memory_search` - Check exclusion list
- `read` - Load ICP criteria

---

## Example Output

```json
[
  {
    "name": "Smart Warehousing",
    "domain": "smartwarehousing.com",
    "revenue_estimate": "$100M",
    "facilities_estimate": 38,
    "industry": "3PL",
    "geography": "US"
  },
  {
    "name": "ShipMonk",
    "domain": "shipmonk.com",
    "revenue_estimate": "$200M",
    "facilities_estimate": 12,
    "industry": "3PL",
    "geography": "US"
  }
]
```

---

## Error Handling

| Scenario | Handling |
|----------|----------|
| No candidates found | Return empty list, log reason |
| Source unavailable | Use backup source, flag if all fail |
| Too many candidates | Cap at 100, return top by revenue |

---

## Next Agent

After completion, output goes to **Human Checkpoint #1** for approval, then to **Agent 2: ICP Qualifier**.
