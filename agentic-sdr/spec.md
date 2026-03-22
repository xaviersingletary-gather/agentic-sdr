# Agentic SDR — GSD Specification
**Version:** 1.0
**Date:** 2026-03-19
**Author:** Xavier Singletary (GTM Engineer)
**Sender Persona:** Rob

---

## Overview

An autonomous sales development system that identifies net-new ICP-fit accounts, enriches them with buying signals, finds and contacts the right personas, and books demos for Rob — without manual prospecting work. Fully autonomous after one-time template and strategy approval.

**Primary KPI:** Demos booked
**Secondary KPI:** Positive reply rate
**Weekly target:** 50 accounts researched → 20–30 contacts enrolled → 10+ demos/month

---

## Actors

| Actor | Role |
|---|---|
| **Xavier** | GTM Engineer — builds, maintains, and monitors the system. Receives 70+ score Slack alerts and routes as needed. |
| **Rob** | Sender persona — all outreach is written and sent in Rob's voice and identity. |
| **The System** | Autonomous agents that research, score, enrich, find contacts, and execute outreach. |
| **The Prospect** | Receives outreach, books a demo. |

---

## User Stories

| Actor | Action | Measurable Outcome |
|---|---|---|
| Xavier | Approves master templates and sequence strategy once | System runs autonomously without per-message approval |
| Xavier | Receives Slack notification when account scores 70+ | Reviews and routes to relevant team member within 24hrs |
| Rob | Is the face of all outreach | Every LinkedIn message, email, and phone flag is in Rob's name |
| System | Discovers net-new ICP-fit companies from scratch | 50 candidate accounts researched per week |
| System | Scores each account against ICP and signal criteria | Accounts below 40 discarded; 40–69 auto-run; 70+ notify Xavier |
| System | Enrolls qualified contacts in multi-channel sequences | Day 0 LinkedIn + email initiated within 24hrs of qualification |
| System | Tracks replies and books demos | Positive replies escalated; demos logged in HubSpot |

---

## ICP Definition

### Floor (minimum to enter pipeline)

| Criteria | Requirement |
|---|---|
| Annual Revenue | $500M+ |
| Facility Count | 11+ distribution or fulfillment centers |
| HQ Geography | North America |
| Vertical | Manufacturing, Food & Bev, Healthcare/Pharma, Retail, 3PL/Logistics |
| WMS in Place | Must have WMS of record (Blue Yonder, Manhattan, SAP, or Tier 2+) |
| EMEA-only | Hard disqualifier |

If any floor criteria fail → discard, do not proceed.

### Quality Score (0–100)

| Signal | Points |
|---|---|
| Active job listing: CI / Automation Engineering / Inventory Control | +25 |
| New DC opening or facility expansion announced | +25 |
| WMS migration underway | +20 |
| Recent audit failure, shrink event, or exec accuracy mandate | +20 |
| Automation footprint exists (AMRs, ASRS, AGVs) | +10 |
| Contact identified as TDM persona | +15 |
| Contact identified as Financial Sponsor persona | +10 |

| Score Range | Action |
|---|---|
| < 40 | Discard |
| 40–69 | Enter pipeline, run autonomously |
| 70+ | Enter pipeline + Slack notification to Xavier |

---

## Exclusion List (Hard Block)

The system checks every discovered account against three lists before proceeding. Any fuzzy name match → hard skip.

**Current Customers (41):**
Ace Endico, Airlite Plastics, Allied Beverage Group, Amazon, Ariat, Army & Air Force Exchange Service (AAFES), Aroplax, Austin Lighthouse, Axon, Barrett Distribution, Bosma Enterprises, Capstone Logistics, Chefs' Warehouse, Cooper Lighting, DNATA, DSV North America, Dalosy, Echo Global Logistics, Geodis, Gordon Food Service, Highline Warren, Hims and Hers Health, Holman Logistics, KeHE: DPI Specialty Foods, Kwik Trip, Langham Logistics, McKinsey & Company, NFI Industries, Peak Technologies, Point B Solutions, Progressive Logistics, Rivian Automotive, Romark Logistics, TJX, Taylor Logistics, Toyota, Vytalogy, Wagner Logistics, Whirlpool, Bosch, Roadtex Transportation

**Strategic Accounts (13):**
Amazon, Capstone Logistics, CEVA Logistics, DHL Group, FedEx, Geodis, GXO, Keurig Dr Pepper, MilliporeSigma, Nestlé, PepsiCo, Procter & Gamble, Target

**Target Accounts (152):**
Full Salesforce-managed list including: 7-Eleven, AbbVie, Adidas, Airbus, Albertsons, Americold, Amgen, Anheuser-Busch, Ashley Furniture, Barry Callebaut, Bayer, Best Buy, BJ's Wholesale, BMW, Boeing, BorgWarner, Bristol Myers Squibb, C&S Wholesale Grocers, Cardinal Health, Cargill, Caterpillar, Cencora, Chewy, Church & Dwight, Cintas, CJ Logistics, Colgate-Palmolive, Costco, CVS, DHL, Disney, Dollar General, DP World, DSV, Dutch Valley Foods, Eli Lilly, FedEx, Ford, General Mills, General Motors, Georgia-Pacific, GSK, GXO, Hershey, Honda, Hormel, Hub Group, Hyundai, IKEA, Ingram Micro, John Deere, Johnson & Johnson, Kaiser Permanente, Kellanova, Kenco, Keurig Dr Pepper, Kia, Kimberly-Clark, Kohl's, Kraft Heinz, Kroger, Kuehne + Nagel, L'Oréal, Lenovo, Lineage Logistics, Lowe's, LVMH, Maersk, Magna International, Mars, Martin Brower, Mastronardi Produce, McKesson, McLane, Medline, Medtronic, Meijer, Merck, MilliporeSigma, Michaels, Nestlé, Nike, Nissan, Nordstrom, Owens & Minor, Pactiv, Penske, PepsiCo, Petco, PetSmart, Pfizer, PPG, Pratt & Whitney, P&G, Revlon, RJW Logistics, RXO, Ryder, Saddle Creek, Sanofi, Sephora, Sherwin-Williams, Siemens, Skechers, Southern Glazer, Stanley Black & Decker, Staples, Starbucks, Stellantis, Subaru, Sysco, Target, TE Connectivity, Tesla, Coca-Cola, Home Depot, Thyssenkrupp, Total Distribution, Tyson Foods, Uline, Unilever, UNFI, UPS, US Foods, Vertical Cold Storage, Volvo, Walgreens, Walmart, Wayfair, Wesco, Williams Sonoma + others

---

## Data Models

### Account
```
company_name        string
domain              string
industry            enum (Manufacturing | Food_Bev | Healthcare_Pharma | Retail | Logistics)
annual_revenue      number
facility_count      number
hq_country          string
wms_detected        bool
automation_footprint bool
icp_score           number (0–100)
quality_score       number (0–100)
status              enum (researching | qualified | disqualified | in_outreach |
                          meeting_booked)
exclusion_reason    enum (null | customer | target | strategic)
created_at          timestamp
last_activity_at    timestamp
```

### Contact
```
first_name          string
last_name           string
title               string
persona_type        enum (TDM | ODM | Financial_Sponsor | IT | Safety | Exec_Sponsor)
linkedin_url        string
email               string
phone               string
verified            bool
outreach_status     enum (pending | enrolled | replied | bounced | opted_out)
last_contacted_at   timestamp
```

### Signal
```
signal_type         enum (job_posting | new_dc | wms_migration | audit_failure |
                          exec_mandate | automation_adoption)
signal_source       enum (Clay | Exa | LinkedIn | news)
signal_date         date
raw_content         string
points_contributed  number
detected_at         timestamp
```

### Outreach
```
channel             enum (LinkedIn | email | phone_flag)
template_id         string
message_content     string
sequence_day        enum (0 | 3 | 7 | 14 | 30)
sent_at             timestamp
status              enum (pending | sent | opened | replied | bounced)
```

---

## Tool Stack

| Function | Tool |
|---|---|
| Company discovery | Exa (web search) + Clay (firmographic lookup) |
| Signal detection | Clay (job postings) + Exa (news, announcements) |
| Contact finding | Apollo + LinkedIn Sales Navigator |
| Email sequences | Apollo (through Rob's connected mailbox) |
| LinkedIn sequences | HeyReach |
| CRM / system of record | HubSpot |
| Notifications | Slack (Xavier's personal channel) |

---

## Agent API Contracts

### Agent 1 — Prospector
```
IN:   icp_criteria (hardcoded), exclusion_list
OUT:  candidates[] { company_name, domain, industry,
                     revenue_est, facility_count, hq_country }
TOOLS: Exa, Clay
GOAL: 50 candidate accounts per weekly run
```

### Agent 2 — ICP Qualifier
```
IN:   candidate_company
OUT:  icp_score (0–100), pass (bool), disqualification_reason
TOOLS: Clay (technographics — WMS, Wi-Fi, automation footprint)
GOAL: Filter to accounts that clear the floor criteria
```

### Agent 3 — Signal Hunter
```
IN:   qualified_company (icp_score ≥ 40)
OUT:  signals[], quality_score (0–100), notify_xavier (bool)
TOOLS: Clay (job postings), Exa (news, expansions, exec mandates)
GOAL: Score signal strength; flag 70+ to Xavier via Slack
```

### Agent 4 — Contact Finder
```
IN:   qualified_company
OUT:  contacts[] { name, title, persona_type, linkedin_url,
                   email, phone, verified }
      priority_contact (TDM first, Financial Sponsor second)
TOOLS: Apollo, LinkedIn Sales Navigator
GOAL: Minimum 1 verified TDM or Financial Sponsor per account
```

### Agent 5 — Outreach Agent
```
IN:   company, contacts, signals, approved_templates
OUT:  sequences_enrolled { linkedin (HeyReach), email (Apollo) }
      hubspot_activity_logged (bool)
TOOLS: HeyReach, Apollo, HubSpot
SEQUENCE:
  Day 0  → LinkedIn connection request + email #1
  Day 3  → LinkedIn follow-up message (if connected)
  Day 7  → Email #2 + phone flag to Rob
  Day 14 → Email #3
  Day 30 → Breakup email
```

### Agent 6 — Follow-up Agent
```
IN:   outreach_history, reply_signals
OUT:  next_action (continue | pause | escalate_to_rob)
      hubspot_updated (bool)
      demo_booked (bool)
TOOLS: HubSpot, Apollo, HeyReach
GOAL: Positive reply → escalate to Rob; demo booked → log in HubSpot
```

---

## Approved Upfront (One-Time)

Before the system runs, Xavier approves:

1. **Email copy templates** — one per sequence day (Days 0, 3, 7, 14, 30), per persona type (TDM, Financial Sponsor)
2. **LinkedIn message templates** — connection request copy + follow-up copy
3. **Sequence structure** — channel order, timing, and cadence
4. **Persona-specific messaging angles** — TDM (proof + integration), Financial Sponsor (ROI + network scale)

---

## Deduplication Rules

- 90-day lookback: no re-contacting the same person within 90 days
- If a company was previously disqualified, do not re-research within 90 days
- If a contact has opted out, permanent block — never re-enroll

---

## Explicit Non-Goals

This system does **not**:

1. Contact any account on the Target, Strategic, or Customer exclusion list
2. Run without approved templates loaded — no templates = no outreach
3. Handle inbound leads or autonomously respond to unsolicited replies
4. Make phone calls — Day 7 phone flag is a notification to Rob only
5. Manage post-demo follow-up — handoff to Rob/AE is the finish line
6. Handle expansion or upsell motions at existing customers
7. Target EMEA-only companies
8. Contact anyone below Director level
9. Re-contact the same person within 90 days
10. Operate without a current exclusion list loaded at runtime
