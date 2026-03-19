# Agentic SDR Workflow - Agent Definitions

This document defines the multi-agent architecture for the Gather AI outbound prospecting engine. Each agent has a specific task, inputs, outputs, and decision criteria.

---

## Workflow Overview

```
Prospector → ICP Qualifier → Signal Hunter → Contact Finder → Contact Enrichment 
→ Account Strategist → [Lead Magnet Creator → Landing Page Agent] → Outreach Agent → Follow-up Agent
```

**Human checkpoints at:** 1, 2, 3, 4, 5, 6, 7, 8

---

## Agent Definitions

---

### Agent 1: Prospector

| Attribute | Value |
|-----------|-------|
| **Name** | Prospector |
| **Task** | Find new companies matching ICP criteria |
| **Trigger** | Scheduled (weekly) or on-demand |
| **Input** | - ICP criteria (revenue, facilities, industry, geography) |
| | - Exclusion list (existing customers, targets, strategic accounts) |
| | - Source lists (ZoomInfo, Crunchbase, trade press) |
| **Output** | `List[Company]` - Raw list of candidate companies |
| **Success Criteria** | Returns 20-100 new candidate companies |
| **Tools** | web_search, web_fetch, memory_search |

**Process:**
1. Query source lists for companies matching ICP
2. Cross-reference against exclusion list
3. Remove duplicates
4. Return candidate list with basic firmographics

---

### Agent 2: ICP Qualifier

| Attribute | Value |
|-----------|-------|
| **Name** | ICP Qualifier |
| **Task** | Score accounts against ICP criteria |
| **Trigger** | After Prospector completes |
| **Input** | `List[Company]` - Output from Prospector |
| **Output** | `List[AccountScore]` - Each account with ICP score (HIGH/MEDIUM/LOW) + reason |
| **Success Criteria** | Every account scored with justification |
| **Tools** | web_search, web_fetch |

**ICP Scoring Matrix:**

| Criteria | HIGH (3) | MEDIUM (2) | LOW (1) | OUT (0) |
|----------|-----------|-------------|---------|---------|
| Revenue | $500M+ | $200-500M | <$200M | - |
| Facilities | 11+ | 5-10 | 1-4 | - |
| Industry | In-scope* | Adjacent | Peripheral | Out |
| WMS | Tier 2+ | Legacy/Unknown | None | - |
| Geography | US/Canada | - | - | Other |

*In-scope: Manufacturing, Food & Bev, Retail, 3PL, Pharma, CPG

---

### Agent 3: Signal Hunter

| Attribute | Value |
|-----------|-------|
| **Name** | Signal Hunter |
| **Task** | Find buying signals for qualified accounts |
| **Trigger** | After human approves HIGH-fit accounts |
| **Input** | `List[AccountScore]` - Approved HIGH accounts |
| **Output** | `SignalReport` per account |
| **Success Criteria** | At least 1 signal found per account |
| **Tools** | web_search, web_fetch |

**Signal Types:**

| Signal | Weight | Evidence Source |
|--------|--------|-----------------|
| New DC opening | 🔥 HIGH | News, press releases |
| Active hiring (CI/Inventory) | 🔥 HIGH | LinkedIn, Indeed |
| WMS migration | 🔥 HIGH | News, earnings calls |
| Audit failure / shrink | 🔥 HIGH | News, SEC filings |
| Competitor deployed tech | MEDIUM | Trade press |
| Executive mandate | MEDIUM | LinkedIn, earnings |
| Automation investment | LOW | News |

---

### Agent 4: Contact Finder

| Attribute | Value |
|-----------|-------|
| **Name** | Contact Finder |
| **Task** | Map buying committee for each account |
| **Trigger** | After Signal Hunter completes |
| **Input** | `SignalReport` - Account with signals |
| **Output** | `BuyingCommittee` - List of personas with names + titles |
| **Success Criteria** | At least TDM identified |
| **Tools** | web_search, web_fetch, LinkedIn |

**Persona Priority:**

| Rank | Persona | Definition |
|------|---------|------------|
| 1 | TDM | VP/Dir Warehouse Ops, Supply Chain Tech, WMS Manager |
| 2 | OCM | VP/Dir Distribution Operations, Fulfillment |
| 3 | FS | CFO, VP Finance, SVP Supply Chain (P&L owner) |
| 4 | IT | IT Lead for Supply Chain/WMS |
| 5 | ES | COO, EVP Operations |

---

### Agent 5: Contact Enrichment

| Attribute | Value |
|-----------|-------|
| **Name** | Contact Enrichment |
| **Task** | Get contact details for buying committee |
| **Trigger** | After Contact Finder maps committee |
| **Input** | `BuyingCommittee` |
| **Output** | `EnrichedContacts` - Names + titles + emails + LinkedIn URLs |
| **Success Criteria** | Contact info for at least TDM + OCM |
| **Tools** | Apollo, ZoomInfo, LinkedIn Sales Navigator |

---

### Agent 6: Account Strategist

| Attribute | Value |
|-----------|-------|
| **Name** | Account Strategist |
| **Task** | Determine best approach for each account |
| **Trigger** | After Contact Enrichment |
| **Input** | `SignalReport` + `EnrichedContacts` + `AccountScore` |
| **Output** | `StrategyRecommendation` - Approach + lead magnet type + channel |
| **Success Criteria** | Clear recommendation with justification |
| **Tools** | Internal reasoning (no external calls) |

**Decision Matrix:**

| Signal Strength | Persona | Recommended Approach |
|----------------|---------|---------------------|
| HIGH (expansion, hiring) | TDM | Direct outreach (no lead magnet) |
| MEDIUM | Any | Lead magnet first |
| WEAK | Any | Nurture track |

**Lead Magnet Selection:**

| Industry | Recommended Lead Magnet |
|----------|-------------------------|
| 3PL | ROI Calculator - "Calculate your contract value at 99.9% accuracy" |
| Food & Bev | Benchmark Report - "Food Distributor Inventory Accuracy Report" |
| Retail | Case Study - "How [similar retailer] improved in-stock availability" |
| Pharma | Compliance Guide - "FDA Audit-Ready Inventory Documentation" |
| Manufacturing | ROI Calculator - "Production Uptime through Inventory Accuracy" |

---

### Agent 7: Lead Magnet Creator

| Attribute | Value |
|-----------|-------|
| **Name** | Lead Magnet Creator |
| **Task** | Create the selected lead magnet asset |
| **Trigger** | After Strategy recommends lead magnet approach |
| **Input** | `StrategyRecommendation` - Includes lead magnet type + account data |
| **Output** | `LeadMagnetAsset` - ROI calculator, PDF report, or case study |
| **Success Criteria** | Complete asset ready for landing page |
| **Tools** | Document creation tools |

**Lead Magnet Templates:**

| Type | Components |
|------|------------|
| ROI Calculator | Input fields (revenue, DCs, SKUs) + formula + peer benchmarks + CTA |
| Benchmark Report | Industry data + peer comparisons + methodology + CTA |
| Case Study | Problem + Solution + Results + CTA |

---

### Agent 8: Landing Page Agent

| Attribute | Value |
|-----------|-------|
| **Name** | Landing Page Agent |
| **Task** | Build personalized landing page |
| **Trigger** | After Lead Magnet Creator completes |
| **Input** | `LeadMagnetAsset` + `AccountData` (company name, revenue, facilities, signals) |
| **Output** | `LandingPage` - URL + content preview |
| **Success Criteria** | Live URL with personalized content |
| **Tools** | Web creation tools |

**Landing Page Components:**

```
Header:
- Company logo/name
- "Personalized for [Company Name]"

Hero:
- Value prop statement
- Company-specific stats

Content Block 1:
- The Lead Magnet
- Interactive calculator OR
- Downloadable report

Content Block 2:
- Peer proof (similar company case study)
- Industry benchmarks

Content Block 3:
- CTA: [Schedule Call] or [Download]

Footer:
- Gather AI branding
```

---

### Agent 9: Outreach Agent

| Attribute | Value |
|-----------|-------|
| **Name** | Outreach Agent |
| **Task** | Execute outreach sequence |
| **Trigger** | After human approves strategy + content |
| **Input** | `LandingPage` + `EnrichedContacts` + `StrategyRecommendation` |
| **Output** | `OutreachSent` - Confirmation of messages sent |
| **Success Criteria** | Messages delivered to all target contacts |
| **Tools** | message, LinkedIn (via browser), email (via SMTP) |

**Outreach Channels:**

| Channel | Best For |
|---------|----------|
| LinkedIn InMail | TDM, OCM (tech-savvy) |
| Email | FS, ES (executives) |
| Multi-channel | All personas |

---

### Agent 10: Follow-up Agent

| Attribute | Value |
|-----------|-------|
| **Name** | Follow-up Agent |
| **Task** | Nurture and follow-up |
| **Trigger** | Scheduled (Day 3, 7, 14 after outreach) |
| **Input** | `OutreachSent` + response data |
| **Output** | `MeetingBooked` or `NurtureTrack` |
| **Success Criteria** | Meeting booked OR moved to nurture |
| **Tools** | message, web_search |

**Follow-up Sequence:**

| Day | Action |
|-----|--------|
| Day 0 | Initial outreach sent |
| Day 3 | "Did you see my message?" - soft follow |
| Day 7 | Share relevant case study |
| Day 14 | "Is now a bad time?" - final attempt |
| Day 30 | Move to nurture track |

---

## Human-in-the-Loop Checkpoints

| # | When | Human Task | Go/No-Go Criteria |
|---|------|-----------|-------------------|
| 1 | After Prospector | Review new lead list | Quality of candidates |
| 2 | After ICP Qualifier | Approve HIGH-fit accounts | ICP score alignment |
| 3 | After Signal Hunter | Approve signal strength | At least 1 HIGH signal |
| 4 | After Contact Finder | Verify persona accuracy | Correct names + titles |
| 5 | After Account Strategist | Approve approach | Strategy makes sense |
| 6 | Before Landing Page | Review personalized content | Brand + accuracy |
| 7 | Before Outreach | Approve message | Tone + personalization |
| 8 | After Follow-up | Review results | Hand off to sales |

---

## Data Models

### Company
```json
{
  "name": "string",
  "domain": "string",
  "revenue": "number",
  "facilities": "number",
  "industry": "string",
  "geography": "string",
  "wms": "string"
}
```

### AccountScore
```json
{
  "company": "Company",
  "icp_fit": "HIGH | MEDIUM | LOW",
  "score_breakdown": {
    "revenue": 3,
    "facilities": 3,
    "industry": 3,
    "wms": 2
  },
  "reason": "string"
}
```

### SignalReport
```json
{
  "company": "Company",
  "signals": [
    {
      "type": "expansion | hiring | wms_migration | audit_failure | competitor",
      "weight": "HIGH | MEDIUM | LOW",
      "evidence": "string",
      "source": "string"
    }
  ],
  "overall_strength": "STRONG | MEDIUM | WEAK"
}
```

### BuyingCommittee
```json
{
  "company": "Company",
  "contacts": [
    {
      "name": "string",
      "title": "string",
      "persona": "TDM | OCM | FS | IT | ES",
      "linkedin_url": "string",
      "email": "string"
    }
  ]
}
```

### StrategyRecommendation
```json
{
  "company": "Company",
  "approach": "DIRECT | LEAD_MAGNET",
  "lead_magnet_type": "ROI_CALCULATOR | BENCHMARK_REPORT | CASE_STUDY | NONE",
  "primary_channel": "LINKEDIN | EMAIL | MULTI",
  "recommended_sequence": [
    {
      "day": 0,
      "action": "string",
      "channel": "string"
    }
  ],
  "persona_priority": ["TDM", "OCM", "FS"]
}
```

---

## Execution Modes

### Batch Mode (Weekly)
- Prospector runs weekly
- Human reviews 20 accounts
- Pipeline continues for approved accounts

### Real-Time Mode (Triggered)
- New lead identified manually
- Fast-track through workflow
- Shorter human review windows

### Parallel Mode
- Multiple accounts through workflow simultaneously
- Each has independent checkpoint gates

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Accounts researched per week | 50 |
| HIGH-ICP accounts | 20 |
| Accounts with signals | 10 |
| Contacts enriched | 30 |
| Meetings booked per month | 10 |

---

## File Structure

```
/agentic-sdr/
├── agents/
│   ├── prospector.md
│   ├── icp_qualifier.md
│   ├── signal_hunter.md
│   ├── contact_finder.md
│   ├── contact_enrichment.md
│   ├── account_strategist.md
│   ├── lead_magnet_creator.md
│   ├── landing_page_agent.md
│   ├── outreach_agent.md
│   └── follow_up_agent.md
├── checkpoints/
│   └── human_review_template.md
├── templates/
│   ├── roi_calculator.md
│   ├── benchmark_report.md
│   └── case_study.md
├── data_models/
│   └── schemas.json
└── workflow.md (this file)
```
