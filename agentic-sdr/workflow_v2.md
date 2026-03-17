# Agentic SDR Workflow v2 - Complete Strategy

**Version:** 2.0  
**Last Updated:** 2026-03-17  
**Purpose:** Automated outbound prospecting engine for Gather AI

---

## Executive Summary

Automated outbound prospecting engine that researches accounts, finds buying signals, identifies contacts, enriches data, and executes multi-channel outreach (LinkedIn + Email + Phone) with the goal of booking meetings through HubSpot.

**Target:** 40 meetings booked/month

---

## Architecture

### 6 Agents

| # | Agent | Model Tier | Task |
|---|-------|-----------|------|
| 1 | **Researcher** | Fast/Cheap | Find companies + signals + contacts |
| 2 | **Qualifier** | Best Reasoning | Score + rank accounts |
| 3 | **Enricher** | Fast + API | Get email + phone |
| 4 | **Strategist** | Best Creative | Create personalized messages |
| 5 | **Outreach Agent** | Reliable | Send + log to HubSpot |
| 6 | **Follow-up Agent** | Good Reasoning | Nurture + book meetings |

---

## Weekly Cadence

| Day | Action |
|-----|--------|
| **Monday** | Researcher finds 50 companies + signals + contacts |
| **Tuesday** | Qualifier scores → Human #1 reviews (approve top 10) |
| **Wednesday** | Enricher + Strategist run in parallel |
| **Thursday** | Human #2 reviews (approve messages) |
| **Friday** | Outreach Agent sends multi-channel |
| **Daily** | Follow-up Agent checks responses, books meetings |

**Output:** 10 accounts/week → 40/month

---

## Human Checkpoints

| # | When | Human Task |
|---|------|------------|
| 1 | Tuesday | Review + approve top 10 HIGH+HOT accounts |
| 2 | Thursday | Review + approve personalized messages |

**Why 2 checkpoints:** Quality control + brand voice, but minimal human time.

---

## Multi-Channel Approach

| Channel | When | Content |
|---------|------|---------|
| **LinkedIn** | Day 0 | Connection request + short message (via HeyReach) |
| **Email** | Day 0 | Personalized email + HubSpot meeting link |
| **Phone** | Day 7 | Warm call (using enriched numbers) |

---

## API Stack

| Function | Tool | Notes |
|----------|------|-------|
| Research + Signals + Enrichment | Clay | Replaces Apollo + ZoomInfo + Clearbit |
| Earnings signals | Exa or Perplexity | Optional - only for earnings |
| LinkedIn outreach | HeyReach | Via Clay native or direct API |
| Email sending | Instantly or Smartlead | For deliverability |
| CRM | HubSpot | Logging + meeting booking |
| Notifications | Slack | Meeting booked alerts |

---

## Agent Definitions

---

### Agent 1: RESEARCHER

```
================================================================================
AGENT: Researcher (v2)
================================================================================

ROLE: Find companies, signals, and contacts in parallel

MODEL TIER: Fast/Cheap (GPT-4o-mini or equivalent)

FREQUENCY: Weekly (Monday)

--------------------------------------------------------------------------------
INPUTS:
--------------------------------------------------------------------------------
- ICP criteria:
  * Revenue: $500M+
  * Facilities: 11+
  * Geography: US/Canada
  * Industries: 3PL, Food & Beverage, Retail, Pharma, Manufacturing, CPG
- Exclusion list (from database)
- Clay API for company search

--------------------------------------------------------------------------------
OUTPUTS:
--------------------------------------------------------------------------------
For each company found:
{
  "company_name": "string",
  "domain": "string",
  "revenue_estimate": "number",
  "facility_count": "number", 
  "industry": "string",
  "signals": [
    {
      "type": "job_post | news | earnings | leadership | expansion",
      "title": "string",
      "date": "YYYY-MM-DD",
      "source": "string",
      "recency_days": number
    }
  ],
  "contacts": [
    {
      "name": "string",
      "title": "string",
      "persona": "TDM | OCM | FS | ES"
    }
  ]
}

--------------------------------------------------------------------------------
PROCESS:
--------------------------------------------------------------------------------
1. CHECK DEDUPLICATION DATABASE
   - Query companies table for domain processed in last 90 days
   - If domain exists AND processed_date > (today - 90 days): SKIP

2. CALL CLAY API
   - Run company search with ICP filters
   - Get job posting signals (last 90 days)
   - Get news signals (last 180 days)
   - Get leadership changes (last 12 months)
   - Find contacts (TDM, OCM names + titles)

3. FALLBACK: EXA API (earnings signals only)
   - Search for earnings mentions of "OTIF", "chargebacks", "fulfillment failures"
   - Add to signals if found

4. RANK BY SIGNAL STRENGTH
   - Sort output by: signal_recency + signal_count
   - Return top 50 companies

--------------------------------------------------------------------------------
DEDUPLICATION RULES:
--------------------------------------------------------------------------------
- Before processing ANY company, check "companies" table
- If domain exists AND status != 'skipped': SKIP
- Write all new companies to database BEFORE outputting

--------------------------------------------------------------------------------
ERROR HANDLING:
--------------------------------------------------------------------------------
- Clay API returns 0 results: Log error + return empty list + notify human
- Clay rate limited: Wait 60s + retry (max 3 retries)
- Exa fails: Continue without earnings signals (not critical)

--------------------------------------------------------------------------------
DATABASE WRITE:
--------------------------------------------------------------------------------
Write to "companies" table:
- company_id (UUID)
- name
- domain (UNIQUE - key for deduplication)
- industry
- revenue_estimate
- facility_count
- signals_json (JSON)
- date_first_seen
- date_last_seen
- status (new | in_progress | completed | skipped)
```

---

### Agent 2: QUALIFIER

```
================================================================================
AGENT: Qualifier (v2)
================================================================================

ROLE: Score and rank accounts based on ICP fit + signal strength

MODEL TIER: Best Reasoning (GPT-4o, Claude 3.5)

FREQUENCY: Weekly (Tuesday)

--------------------------------------------------------------------------------
INPUTS:
--------------------------------------------------------------------------------
- 50 companies from Researcher
- Signal data for each company

--------------------------------------------------------------------------------
OUTPUTS:
--------------------------------------------------------------------------------
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

--------------------------------------------------------------------------------
SCORING MATRIX:
--------------------------------------------------------------------------------

| Criteria          | Points | Notes                           |
|-------------------|--------|---------------------------------|
| Revenue $500M+    | 3      |                                 |
| Revenue $200-500M | 2      |                                 |
| Revenue <$200M   | 0      | OUT - skip                      |
| 11+ facilities    | 3      |                                 |
| 5-10 facilities   | 2      |                                 |
| 1-4 facilities   | 0      | OUT - skip                      |
| In-scope industry| 2      | 3PL/F&B/Retail/Pharma/Mfg/CPG  |
| Adjacent industry| 1      |                                 |
| Out of scope     | 0      |                                 |

SIGNAL SCORING (with recency multiplier):
- Signal within 30 days:      +3 points
- Signal within 60 days:      +2 points  
- Signal within 90 days:      +1 point
- Signal 90+ days old:        +0 points (ignore)

| Total Score | Classification |
|-------------|---------------|
| 8-12        | HOT - Prioritize |
| 5-7         | WARM |
| 0-4         | COLD - Skip |

--------------------------------------------------------------------------------
RULES:
--------------------------------------------------------------------------------
1. HARD REJECT: Revenue <$200M OR facilities <5 OR out of scope industry
2. ONLY return HOT accounts for human review
3. If no HOT accounts found, return top 5 WARM with explanation
4. Include recency date for each signal in output

--------------------------------------------------------------------------------
DEDUPLICATION CHECK:
--------------------------------------------------------------------------------
- Check "companies" table
- If company has status="human_review_pending" OR "approved": SKIP

--------------------------------------------------------------------------------
DATABASE WRITE:
--------------------------------------------------------------------------------
Update "companies" table:
- score
- classification
- status = "human_review_pending" (if HOT)
- status = "rejected" (if COLD)
```

---

### Agent 3: ENRICHER

```
================================================================================
AGENT: Enricher (v2)
================================================================================

ROLE: Get contact details for approved accounts

MODEL TIER: Fast + API Access

FREQUENCY: Weekly (Wednesday) - parallel with Strategist

--------------------------------------------------------------------------------
INPUTS:
--------------------------------------------------------------------------------
- Approved accounts from Human #1 (top 10)
- Contact names from Researcher

--------------------------------------------------------------------------------
OUTPUTS:
--------------------------------------------------------------------------------
For each contact:
{
  "company_name": "string",
  "contact_name": "string",
  "title": "string",
  "persona": "TDM | OCM | FS | ES",
  "email": "string or null",
  "email_verified": boolean,
  "phone": "string or null",
  "phone_type": "direct | mobile | main | null",
  "linkedin_url": "string or null"
}

Enrichment status summary:
{
  "total_contacts": number,
  "email_found": number,
  "phone_found": number,
  "fully_enriched": number,
  "failed": number
}

--------------------------------------------------------------------------------
PRIMARY SOURCE: CLAY API
--------------------------------------------------------------------------------
- Clay's internal waterfall: tries multiple sources until verified email found
- Returns: email (verified), phone, LinkedIn URL

--------------------------------------------------------------------------------
VALIDATION RULES:
--------------------------------------------------------------------------------
- Email: Must be verified (Clay marks verified/unverified)
- Phone: Prefer direct dials over main company numbers
- If no email found: Mark as "manual_research_needed"

--------------------------------------------------------------------------------
RATE LIMITING:
--------------------------------------------------------------------------------
- Implement 36ms delay between requests
- If rate limited: Wait 60s + retry (max 2 retries)

--------------------------------------------------------------------------------
SUPPRESSION CHECK (MANDATORY):
--------------------------------------------------------------------------------
- Before ANY enrichment, check suppressions table
- If email in suppressions: SKIP entirely
- Log to follow_up_log with reason

--------------------------------------------------------------------------------
DATABASE WRITE:
--------------------------------------------------------------------------------
Write to "contacts" table:
- contact_id (UUID)
- company_id (FK)
- name
- title
- persona
- email
- email_verified
- phone
- phone_type
- linkedin_url
- hubspot_contact_id (null until outreach)
- current_sequence_day = 0
- next_action_date = null
- sequence_status = 'new'

Update "companies" status:
- If 1+ contacts enriched: status = "enriched"
- If all failed: status = "enrichment_failed"
```

---

### Agent 4: STRATEGIST

```
================================================================================
AGENT: Strategist (v2)
================================================================================

ROLE: Create personalized outreach messages

MODEL TIER: Best Creative (GPT-4o, Claude 3.5)

FREQUENCY: Wednesday (parallel with Enricher)

--------------------------------------------------------------------------------
INPUTS:
--------------------------------------------------------------------------------
- Account signals from Qualifier
- Enriched contacts from Enricher
- Industry context (from MEMORY.md)

--------------------------------------------------------------------------------
OUTPUTS:
--------------------------------------------------------------------------------
For each contact:
{
  "company_name": "string",
  "contact_name": "string",
  "persona": "TDM | OCM | FS | ES",
  "linkedin_message_variants": [
    {
      "id": "A | B | C",
      "text": "string (under 150 words)",
      "signal_referenced": "string"
    }
  ],
  "email": {
    "subject": "string",
    "body": "string (under 200 words)"
  },
  "pain_point": "string",
  "meeting_ask": "string",
  "recommended_variant": "A | B | C"
}

--------------------------------------------------------------------------------
PERSONALIZATION RULES:
--------------------------------------------------------------------------------

TDM (Technical Decision Maker):
- Titles: VP/Dir Warehouse Technology, Supply Chain Tech, WMS Manager
- Language: Technical (WMS, inventory accuracy, digital twin, scan)
- Pain points: Data-reality gap, cycle count labor, WMS optimization
- Peer proof: Use other 3PLs or similar companies

OCM (Operational Decision Maker):
- Titles: VP/Dir Distribution Operations, Fulfillment
- Language: Operational (OTIF, chargebacks, throughput, labor)
- Pain points: Fulfillment failures, retailer penalties, labor scarcity
- Peer proof: Use same-industry examples

FS (Financial Sponsor):
- Titles: CFO, VP Finance, SVP Supply Chain (P&L owner)
- Language: ROI, working capital, safety stock
- Pain points: Safety stock bloat, shrink, audit failures
- Peer proof: Use ROI numbers

ES (Executive Sponsor):
- Titles: COO, EVP Operations
- Language: Strategic, competitive position
- Pain points: Scale challenges, network visibility

--------------------------------------------------------------------------------
MESSAGE VARIANT SELECTION:
--------------------------------------------------------------------------------
- Generate 3 variants (A, B, C):
  * Variant A: Pain-focused
  * Variant B: ROI-focused  
  * Variant C: Peer proof-focused
- DEFAULT: Recommend A (pain-focused) unless signal suggests otherwise
- Human will select during checkpoint #2

--------------------------------------------------------------------------------
ALWAYS INCLUDE:
--------------------------------------------------------------------------------
- 1-2 specific signal references (from signals input)
- HubSpot meeting link
- CTA: 15-min call request

--------------------------------------------------------------------------------
ERROR HANDLING:
--------------------------------------------------------------------------------
- No signals for company: Use generic industry pain point
- No contact title: Use "operations leader" as fallback
- Meeting link missing: ERROR - stop and alert human

--------------------------------------------------------------------------------
DATABASE WRITE:
--------------------------------------------------------------------------------
Write to "message_templates" table:
- template_id (UUID)
- contact_id (FK)
- linkedin_variant_a
- linkedin_variant_b
- linkedin_variant_c
- email_subject
- email_body
- selected_variant (null until human selects)
- approved = FALSE
- created_date
```

---

### Agent 5: OUTREACH AGENT

```
================================================================================
AGENT: Outreach Agent (v2)
================================================================================

ROLE: Execute multi-channel outreach and log to HubSpot

MODEL TIER: Reliable + API Capable

FREQUENCY: Weekly (Friday)

--------------------------------------------------------------------------------
INPUTS:
--------------------------------------------------------------------------------
- Approved message templates from Human #2
- Enriched contacts with emails/phones
- HubSpot meeting link
- HubSpot API key
- HeyReach API key + campaign ID
- Instantly/Smartlead API key (email)

--------------------------------------------------------------------------------
OUTPUTS:
--------------------------------------------------------------------------------
{
  "sent_count": number,
  "failed_count": number,
  "details": [
    {
      "contact_name": "string",
      "company_name": "string",
      "channel": "linkedin | email",
      "status": "sent | failed",
      "timestamp": "ISO date",
      "hubspot_contact_id": "string or null",
      "heyreach_message_id": "string or null"
    }
  ]
}

--------------------------------------------------------------------------------
SEND SEQUENCE:
--------------------------------------------------------------------------------
STEP 1: HeyReach API → LinkedIn (morning)
- Call HeyReach API: POST /messages/send
- Payload: { linkedin_url, message, campaign_id }
- Store HeyReach message_id in outreach_log

STEP 2: Email via Instantly/Smartlead (afternoon, 4 hours later)
- Send personalized email with meeting link
- Log to HubSpot

--------------------------------------------------------------------------------
SUPPRESSION CHECK (MANDATORY):
--------------------------------------------------------------------------------
- Before sending ANY message, check suppressions table
- If email in suppressions: SKIP + log warning
- If contact has sequence_status = 'opted_out': SKIP

--------------------------------------------------------------------------------
RATE LIMITING (CRITICAL):
--------------------------------------------------------------------------------
- HeyReach: Max 30 connection requests per day (enforced by HeyReach)
- Email: Max 100 per day
- Implement 20-minute delay between channels
- HARD STOP at 5pm local time (no evening sends)

--------------------------------------------------------------------------------
HUBSPOT LOGGING:
--------------------------------------------------------------------------------
For each contact:
1. CREATE/UPDATE CONTACT
   - Fields: name, email, company, phone, persona
   - List: "SDR Outbound"

2. LOG OUTREACH ACTIVITY
   - Activity type: "Outreach Sent"
   - Include: message copy, channel, timestamp

3. SET PROPERTIES
   - lifecycle_stage: "lead"
   - hs_lead_status: "Attempted to Contact"
   - next_follow_up: (today + 3 days)

--------------------------------------------------------------------------------
DATABASE WRITE:
--------------------------------------------------------------------------------
Write to "outreach_log" table:
- outreach_id (UUID)
- contact_id (FK)
- company_id (FK)
- channel
- sequence_day = 0
- message_copy (truncated)
- sent_timestamp
- hubspot_activity_id
- heyreach_message_id
- status

Update "contacts" table:
- last_outreach_date = today
- outreach_count + 1
- current_sequence_day = 0
- next_action_date = today + 3 days
- sequence_status = 'active'
```

---

### Agent 6: FOLLOW-UP AGENT

```
================================================================================
AGENT: Follow-up Agent (v2)
================================================================================

ROLE: Nurture contacts and book meetings

MODEL TIER: Good Reasoning

FREQUENCY: Daily (runs every morning)

--------------------------------------------------------------------------------
INPUTS:
--------------------------------------------------------------------------------
- Outreach log from Outreach Agent
- HubSpot contact responses (via API)
- HubSpot meeting link

--------------------------------------------------------------------------------
OUTPUTS:
--------------------------------------------------------------------------------
{
  "meetings_booked": number,
  "replies_received": number,
  "follow_ups_sent": number,
  "moved_to_nurture": number,
  "details": [...]
}

--------------------------------------------------------------------------------
QUERY LOGIC:
--------------------------------------------------------------------------------
Find contacts where:
- sequence_status = 'active'
- next_action_date <= today

--------------------------------------------------------------------------------
SEQUENCE LOGIC:
--------------------------------------------------------------------------------

| Day | Condition | Action |
|-----|-----------|--------|
| 3   | No response | LinkedIn: "Did you see my message?" |
| 7   | No response | Email + Phone call |
| 14  | No response | Email: "Last attempt" |
| 30  | No response | Move to nurture |

RESPONSE HANDLING:
- "Interested" → Log → Notify human immediately
- "Meeting requested" → Log meeting → Update HubSpot stage
- "Not now" → Log + pause 60 days
- "Not interested" → Add to suppressions + log
- "Unsubscribe" → Add to suppressions + never contact again

--------------------------------------------------------------------------------
PHONE CALLS:
--------------------------------------------------------------------------------
- ONLY during business hours (9am-5pm)
- Max 10 calls per day
- Use enriched phone numbers
- Log outcome to follow_up_log

--------------------------------------------------------------------------------
RATE LIMITING:
--------------------------------------------------------------------------------
- Max 30 follow-ups per day total
- Max 10 phone calls per day
- HARD STOP after Day 14 (3 attempts max)

--------------------------------------------------------------------------------
HUBSPOT ACTIONS:
--------------------------------------------------------------------------------
MEETING BOOKED:
- Log "Meeting Scheduled" activity
- Update stage: "Lead" → "Meeting Booked"
- Notify human via Slack

REPLY RECEIVED:
- Log "Reply Received"
- Tag contact with sentiment
- Notify human

MOVED TO NURTURE (Day 30):
- Update lifecycle_stage: "lead" → "marketingqualifiedlead"
- Add to "Nurture" list
- sequence_status = 'nurturing'

--------------------------------------------------------------------------------
DATABASE WRITE:
--------------------------------------------------------------------------------
Write to "follow_up_log" table:
- follow_up_id (UUID)
- contact_id (FK)
- sequence_day
- channel
- message_copy
- response (interested | not_interested | not_now | no_response)
- timestamp

Update "contacts" table:
- last_follow_up_date = today
- follow_up_count + 1
- current_sequence_day = sequence_day
- next_action_date = (next sequence date)
- sequence_status (if meeting booked: 'booked', if 30 days no response: 'nurturing')
```

---

## Database Schema

```sql
-- COMPANIES: Deduplication layer for Researcher
CREATE TABLE companies (
  company_id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  domain TEXT UNIQUE NOT NULL,
  industry TEXT,
  revenue_estimate TEXT,
  facility_count INTEGER,
  score INTEGER,
  classification TEXT,
  signals_json JSON,
  date_first_seen DATE DEFAULT CURRENT_DATE,
  date_last_seen DATE DEFAULT CURRENT_DATE,
  status TEXT DEFAULT 'new'
);

-- CONTACTS: With sequence tracking
CREATE TABLE contacts (
  contact_id UUID PRIMARY KEY,
  company_id UUID REFERENCES companies(company_id),
  name TEXT NOT NULL,
  title TEXT,
  persona TEXT,
  email TEXT,
  email_verified BOOLEAN DEFAULT FALSE,
  phone TEXT,
  phone_type TEXT,
  linkedin_url TEXT,
  
  -- Sequence tracking
  current_sequence_day INTEGER DEFAULT 0,
  next_action_date DATE,
  sequence_status TEXT DEFAULT 'new',
  
  -- Outreach tracking
  last_outreach_date DATE,
  outreach_count INTEGER DEFAULT 0,
  last_follow_up_date DATE,
  follow_up_count INTEGER DEFAULT 0,
  
  -- HubSpot sync
  hubspot_contact_id TEXT,
  
  created_date DATE DEFAULT CURRENT_DATE,
  updated_date DATE DEFAULT CURRENT_DATE
);

-- MESSAGE TEMPLATES: With selection tracking
CREATE TABLE message_templates (
  template_id UUID PRIMARY KEY,
  contact_id UUID REFERENCES contacts(contact_id),
  linkedin_variant_a TEXT,
  linkedin_variant_b TEXT,
  linkedin_variant_c TEXT,
  email_subject TEXT,
  email_body TEXT,
  selected_variant CHAR(1),
  approved BOOLEAN DEFAULT FALSE,
  created_date DATE DEFAULT CURRENT_DATE
);

-- OUTREACH LOG: History of all sends
CREATE TABLE outreach_log (
  outreach_id UUID PRIMARY KEY,
  contact_id UUID REFERENCES contacts(contact_id),
  company_id UUID REFERENCES companies(company_id),
  channel TEXT,
  sequence_day INTEGER,
  message_copy TEXT,
  sent_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  hubspot_activity_id TEXT,
  heyreach_message_id TEXT,
  status TEXT DEFAULT 'sent'
);

-- SUPPRESSIONS: Opt-out tracking (LEGAL REQUIREMENT)
CREATE TABLE suppressions (
  suppression_id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  phone TEXT,
  reason TEXT,
  date_added DATE DEFAULT CURRENT_DATE,
  source TEXT
);

-- FOLLOW-UP LOG: Sequence history
CREATE TABLE follow_up_log (
  follow_up_id UUID PRIMARY KEY,
  contact_id UUID REFERENCES contacts(contact_id),
  sequence_day INTEGER,
  channel TEXT,
  message_copy TEXT,
  response TEXT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AGENT STATE: Tracking
CREATE TABLE agent_state (
  agent_name TEXT PRIMARY KEY,
  last_run_date DATE,
  last_run_status TEXT,
  records_processed INTEGER DEFAULT 0,
  errors JSON DEFAULT '[]'
);
```

---

## Environment Variables

```bash
# Core Platform
CLAY_API_KEY=your_key_here
HUBSPOT_API_KEY=your_key_here
HUBSPOT_MEETING_URL=https://meetings.hubspot.com/your-name

# Email
INSTANTLY_API_KEY=your_key_here

# LinkedIn (via HeyReach)
HEYREACH_API_KEY=your_key_here
HEYREACH_CAMPAIGN_ID=your_campaign_id

# Earnings Signals (optional)
EXA_API_KEY=your_key_here

# Notifications
SLACK_WEBHOOK_URL=your_webhook

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/sdr_db
```

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Accounts researched/week | 50 |
| HIGH+HOT accounts approved | 10 |
| Contacts enriched | 20 |
| Outreach messages sent | 20 |
| Meetings booked/month | 40 |
| Reply rate | 15%+ |

---

## File Structure

```
/agentic-sdr/
├── workflow_v2.md           ← This file
├── database/
│   └── schema.sql
├── config/
│   └── env.example
├── agents/
│   ├── 01_researcher.md
│   ├── 02_qualifier.md
│   ├── 03_enricher.md
│   ├── 04_strategist.md
│   ├── 05_outreach_agent.md
│   └── 06_follow_up_agent.md
└── integrations/
    ├── hubspot.md
    ├── heyreach.md
    └── clay.md
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| 2 human checkpoints | Quality control without bottleneck |
| Clay for enrichment | Replaces 3+ tools, simpler stack |
| HeyReach for LinkedIn | Safe automation, no ban risk |
| Sequence tracking in DB | Enables daily follow-up agent |
| Suppressions table | Legal compliance (CAN-SPAM/GDPR) |
| Signal recency scoring | Prioritize recent signals |
| Weekly cadence | Predictable human workload |
| 6 agents (not 10) | Simplified, faster execution |
