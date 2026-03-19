# Agent 4: Contact Finder

## Role Definition

| Attribute | Value |
|-----------|-------|
| **Name** | Contact Finder |
| **Type** | Research Agent |
| **Task** | Map buying committee for each account |
| **Trigger** | After Signal Hunter + Human #3 approval |
| **Position in Workflow** | Step 4 of 10 |

---

## Purpose

The Contact Finder identifies the right people at the target company who make up the buying committee. This is critical for multi-threaded outreach and understanding decision-making dynamics.

---

## Input

```
SignalReport per account:
- Company details
- Signals found
- Overall signal strength
```

---

## Output

```
BuyingCommittee per account:
- Company details
- List of personas identified:
  - Name
  - Title
  - Persona type (TDM, OCM, FS, IT, ES)
  - LinkedIn URL (if found)
```

---

## Persona Definitions

| Persona | Definition | Typical Titles |
|---------|------------|---------------|
| **TDM** | Technical Decision Maker - evaluates and champions the tech | VP/Dir Warehouse Technology, VP/Dir Supply Chain Tech, WMS Manager, Director of CI |
| **OCM** | Operational Decision Maker - owns adoption and floor-level ROI | VP/Dir Distribution Operations, VP/Dir Fulfillment |
| **FS** | Financial Sponsor - controls budget | CFO, VP Finance, SVP Supply Chain (P&L owner) |
| **IT** | IT Stakeholder - integration gatekeeper | IT Director Supply Chain, WMS Manager |
| **ES** | Executive Sponsor - final call on network commitments | COO, EVP Operations, Chief Supply Chain Officer |

---

## Persona Priority

| Rank | Persona | Target First? | Rationale |
|------|---------|---------------|-----------|
| 1 | TDM | ✅ YES | Always first - champion and evaluator |
| 2 | OCM | ✅ YES | Fast follow - validates floor fit |
| 3 | FS | ⚠️ AFTER TDM | Must engage before Stage 3 (deal killer if missed) |
| 4 | IT | ⚠️ LATE | Entry only for new logo |
| 5 | ES | ❌ LATE | Expansion persona - not for new logo |

---

## Research Process

### Step 1: Identify TDM
Search for:
- "VP of Operations [Company]"
- "Director of Warehouse [Company]"
- "Director of Supply Chain [Company]"
- "WMS Manager [Company]"
- "Continuous Improvement Manager [Company]"

### Step 2: Identify OCM
Search for:
- "VP of Distribution [Company]"
- "VP of Fulfillment [Company]"
- "Director of DC Operations [Company]"

### Step 3: Identify FS
Search for:
- "CFO [Company]"
- "VP of Finance [Company]"
- "SVP Supply Chain [Company]" (if P&L owner)

### Step 4: Identify IT
Search for:
- "IT Director [Company] Supply Chain"
- "WMS IT [Company]"

### Step 5: Identify ES
Search for:
- "COO [Company]"
- "EVP Operations [Company]"
- "CEO [Company]" (for smaller companies)

---

## Sources

| Source | Best For |
|--------|----------|
| LinkedIn | Titles, org structure |
| Company "Our Team" page | Leadership names |
| ZoomInfo | Contact details |
| Press releases | Executive appointments |

---

## Example Output

```json
{
  "company": {
    "name": "Cheney Brothers",
    "domain": "cheneybrothers.com"
  },
  "contacts": [
    {
      "name": "Cecil King",
      "title": "VP Operations",
      "persona": "TDM",
      "linkedin_url": "https://linkedin.com/in/cecil-king-xxx",
      "source": "LinkedIn"
    },
    {
      "name": "Peter Borradaile",
      "title": "Director of Operations",
      "persona": "OCM",
      "linkedin_url": "https://linkedin.com/in/peter-borradaile-xxx",
      "source": "LinkedIn"
    },
    {
      "name": "[Name to find]",
      "title": "CFO",
      "persona": "FS",
      "linkedin_url": "",
      "source": "Not found"
    }
  ]
}
```

---

## Quality Indicators

| Indicator | Meaning |
|----------|---------|
| ✅ | Contact found with high confidence |
| ⚠️ | Title matches but name uncertain |
| ❌ | Not found - requires manual research |

---

## Success Criteria

| Metric | Target |
|--------|--------|
| TDM found | >80% of accounts |
| 2+ personas found | >60% of accounts |
| LinkedIn URLs | >70% of contacts |

---

## Tools Used

- `web_search` - Find people
- `web_fetch` - Get company team pages
- `browser` - Navigate LinkedIn

---

## Next Agent

After completion, output goes to **Agent 5: Contact Enrichment** for contact details, then to **Human Checkpoint #4**.
