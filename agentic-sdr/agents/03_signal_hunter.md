# Agent 3: Signal Hunter

## Role Definition

| Attribute | Value |
|-----------|-------|
| **Name** | Signal Hunter |
| **Type** | Research Agent |
| **Task** | Find buying signals for qualified accounts |
| **Trigger** | After ICP Qualifier + Human #2 approval |
| **Position in Workflow** | Step 3 of 10 |

---

## Purpose

The Signal Hunter takes HIGH-fit accounts and identifies signals that indicate the company is in-market or about to be in-market for solutions like Gather AI. These signals help prioritize accounts and inform outreach strategy.

---

## Input

```
List[AccountScore] - HIGH-fit accounts from ICP Qualifier
- Company details
- ICP fit score
- Reason for scoring
```

---

## Output

```
SignalReport per account:
- Company details
- Signals found (type, weight, evidence, source)
- Overall signal strength (STRONG/MEDIUM/WEAK)
```

---

## Signal Types

### 🔥 HIGH-Weight Signals

| Signal | Description | Evidence Sources |
|--------|-------------|------------------|
| **New DC Opening** | Announced new distribution center | News, press releases, LinkedIn |
| **Active Hiring (CI/Inventory)** | Job postings for CI, Inventory Control, Automation | Indeed, LinkedIn, company careers page |
| **WMS Migration/Upgrade** | Publicly announced WMS change | News, earnings calls |
| **Audit Failure / Shrink Event** | Publicly disclosed inventory issues | News, SEC filings |
| **Executive Mandate** | CEO/COO publicly posted about pain | LinkedIn |

### ⚡ MEDIUM-Weight Signals

| Signal | Description | Evidence Sources |
|--------|-------------|------------------|
| **Automation Investment** | Mentioned robotics/automation | News, press releases |
| **Competitor Deployed Tech** | Peer company using autonomous solutions | Trade press |
| **Acquisition** | Merged or acquired facilities | News |
| **Expansion** | Growing footprint | News, LinkedIn |

### ○ LOW-Weight Signals

| Signal | Description | Evidence Sources |
|--------|-------------|------------------|
| **General Growth** | Revenue growth mentioned | Earnings, news |
| **Industry Trends** | Posting about industry challenges | LinkedIn, blog |

---

## Research Process

### Step 1: News Search
For each account, search for:
- "[Company] distribution center expansion"
- "[Company] new warehouse"
- "[Company] hiring inventory"
- "[Company] WMS"
- "[Company] automation"

### Step 2: Job Posting Analysis
Search Indeed, LinkedIn, company careers page for:
- "Inventory Manager"
- "Continuous Improvement"
- "Warehouse Automation"
- "WMS"

### Step 3: Earnings Call Review
For public companies, search:
- SEC filings (10-K)
- Earnings transcripts
- Look for: "inventory accuracy", "shrink", "OTIF", "fulfillment"

### Step 4: Social Listening
Search LinkedIn for:
- Executive posts about challenges
- Company posts about milestones

### Step 5: Compile Signal Report
Document all signals found with:
- Type (expansion, hiring, pain, etc.)
- Weight (HIGH, MEDIUM, LOW)
- Evidence (quote or summary)
- Source (URL)

---

## Signal Strength Calculation

```
STRONG = 2+ HIGH signals OR 1 HIGH + 2+ MEDIUM signals
MEDIUM = 1 HIGH signal OR 2+ MEDIUM signals
WEAK = 1 MEDIUM signal OR no signals found
NONE = No signals found
```

---

## Example Output

```json
{
  "company": {
    "name": "Cheney Brothers",
    "domain": "cheneybrothers.com"
  },
  "signals": [
    {
      "type": "expansion",
      "weight": "HIGH",
      "evidence": "New 386,000 sq ft Florence, SC facility opened late 2024",
      "source": "https://news.example.com/cheney-florence"
    },
    {
      "type": "expansion",
      "weight": "HIGH",
      "evidence": "$1.1B cold storage facility with 45 loading docks",
      "source": "https://news.example.com/cheney-cold-storage"
    },
    {
      "type": "hiring",
      "weight": "HIGH",
      "evidence": "280 jobs created in 2024, multiple warehouse roles",
      "source": "indeed.com/cheney-brothers"
    }
  ],
  "overall_strength": "STRONG"
}
```

---

## Decision Rules

| Strength | Action |
|----------|--------|
| STRONG | Proceed to Contact Discovery |
| MEDIUM | Proceed, but flag for lead magnet approach |
| WEAK | Flag for nurture track |
| NONE | Do not proceed |

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Accounts researched | 100% of input |
| At least 1 signal | >70% of accounts |
| HIGH signals found | >30% of accounts |

---

## Tools Used

- `web_search` - Find news and job postings
- `web_fetch` - Get detailed information
- `memory_search` - Check for prior research

---

## Next Agent

After completion, output goes to **Human Checkpoint #3** for approval, then to **Agent 4: Contact Finder**.
