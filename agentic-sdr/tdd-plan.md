# Agentic SDR — TDD Execution Plan
**Version:** 1.0
**Date:** 2026-03-19

Each phase ends with two hard conditions:
1. All automated tests pass (no exceptions)
2. A human-interpretable demo Xavier can verify

Quality gates apply at the end of every phase:
- Anti-pattern check (structural issues, security vulnerabilities, N+1 queries)
- Linter (zero errors)
- Full test suite (all tests pass)

---

## Phase 1 — Foundation & Data Layer
**Deliverable:** Project scaffold, data models, exclusion list engine

### What gets built
- Project structure (Python, SQLite, pytest, .env config)
- Data models: Account, Contact, Signal, Outreach (SQLite via SQLAlchemy)
- Exclusion list loader — reads all 3 lists (customers, strategic, target)
- Fuzzy match engine — checks any company name against exclusion list
- HubSpot client wrapper (read + write activity)

### Test Criteria
```
✓ All 4 data models create, read, update, delete without error
✓ Exclusion check: "Amazon" → blocked (customer + strategic)
✓ Exclusion check: "PepsiCo" → blocked (strategic + target)
✓ Exclusion check: "Acme Logistics Co" → not blocked (net-new)
✓ Fuzzy match catches "Geodis NA" as matching "Geodis"
✓ Fuzzy match catches "P&G" as matching "Procter & Gamble"
✓ HubSpot client: can read a contact, write an activity log
```

### Demo
Given a list of 10 company names (mix of excluded and net-new), system correctly labels each as blocked or eligible and explains why.

---

## Phase 2 — Prospector + ICP Qualifier
**Deliverable:** Agent 1 + Agent 2 running end-to-end

### What gets built
- Prospector agent — calls Exa (web search) + Clay (firmographics) to find candidate companies matching ICP criteria
- ICP Qualifier agent — scores each candidate against floor criteria and technographic signals
- Exclusion check wired in — disqualified accounts never proceed
- Results persisted to Account table with status + icp_score

### Test Criteria
```
✓ Prospector returns ≥ 10 candidate companies per run
✓ Every candidate has: name, domain, industry, revenue_est, facility_count, hq_country
✓ ICP Qualifier correctly disqualifies: revenue < $500M → discard
✓ ICP Qualifier correctly disqualifies: < 11 facilities → discard
✓ ICP Qualifier correctly disqualifies: EMEA-only HQ → discard
✓ Exclusion list check runs before qualification (not after)
✓ All qualified accounts written to Account table with icp_score
✓ No account on exclusion list ever reaches status = qualified
```

### Demo
Live run: system searches for ICP-fit companies from scratch, returns 10+ candidates, scores them, correctly filters disqualified ones. Xavier reviews the output list — company names, scores, pass/fail reasons.

---

## Phase 3 — Signal Hunter + Slack Notification
**Deliverable:** Agent 3 running, quality scores computed, Xavier gets notified

### What gets built
- Signal Hunter agent — queries Clay (job postings) + Exa (news) for each qualified account
- Signal scoring engine — maps signal types to points, computes quality_score (0–100)
- Slack notification — fires to Xavier's personal channel when quality_score ≥ 70
- Signal records persisted to Signal table

### Test Criteria
```
✓ Job posting (CI/Automation/Inventory) → +25 points
✓ New DC announcement → +25 points
✓ WMS migration signal → +20 points
✓ Audit failure / shrink event signal → +20 points
✓ Automation footprint → +10 points
✓ quality_score = sum of all matched signals (capped at 100)
✓ Account with quality_score < 40 → status = disqualified
✓ Account with quality_score 40–69 → status = qualified, no notification
✓ Account with quality_score ≥ 70 → status = qualified + Slack message fires
✓ Slack message contains: company name, score, top signals, link to HubSpot record
```

### Demo
Run signal detection on 5 qualified accounts. Xavier receives a Slack notification for any that score 70+. Message shows company name, score breakdown, and top signals detected.

---

## Phase 4 — Contact Finder
**Deliverable:** Agent 4 running, verified contacts with persona labels

### What gets built
- Contact Finder agent — queries Apollo + Sales Navigator for each qualified account
- Persona classifier — maps job titles to persona types (TDM, ODM, Financial Sponsor, etc.)
- Director-level floor enforced — no contacts below Director
- 90-day deduplication check — skip contacts already in outreach within 90 days
- Contacts persisted to Contact table with verified flag

### Test Criteria
```
✓ Returns ≥ 1 verified contact per account (email or LinkedIn URL confirmed)
✓ Priority order: TDM first, Financial Sponsor second
✓ "Head of Engineering & Automation" → persona_type = TDM
✓ "VP of Operations" → persona_type = ODM
✓ "EVP Supply Chain" → persona_type = Financial_Sponsor
✓ "Coordinator" or "Analyst" → rejected (below Director floor)
✓ Contact last outreached < 90 days ago → skipped, not enrolled
✓ All contacts written to Contact table with persona_type + verified = true/false
```

### Demo
Given 3 qualified accounts, system returns a contact card for each: name, title, persona type, LinkedIn URL, email (masked for demo), verified status. Xavier confirms persona labels look correct.

---

## Phase 5 — Outreach Agent
**Deliverable:** Agent 5 running, sequences enrolled in HeyReach + Apollo, HubSpot logged

### What gets built
- Template loader — reads approved email + LinkedIn templates from config
- Persona-specific message builder — selects correct template angle per contact persona
- HeyReach integration — enrolls contact in LinkedIn sequence
- Apollo integration — enrolls contact in email sequence
- HubSpot logger — creates activity record for every enrolled contact
- Sequence structure enforced: Day 0 / 3 / 7 / 14 / 30

### Test Criteria
```
✓ No outreach fires without approved templates loaded (hard gate)
✓ TDM contact → receives TDM-angled template (proof + integration messaging)
✓ Financial Sponsor contact → receives FS-angled template (ROI + network scale)
✓ Day 0: LinkedIn connection request + email both enqueued
✓ Day 3: LinkedIn follow-up enqueued (conditional on connection accepted)
✓ Day 7: Email #2 + phone_flag logged in HubSpot (no auto-dial)
✓ Day 14: Email #3 enqueued
✓ Day 30: Breakup email enqueued
✓ HubSpot activity created for every enrolled contact
✓ Dedup check: contact already in active sequence → not re-enrolled
✓ All outreach records written to Outreach table
```

### Demo
Dry-run mode (no real sends): system takes 2 qualified accounts with contacts, selects correct templates, shows Xavier exactly what would be sent to whom on which day. HubSpot shows activity logged. Xavier approves the actual templates before live mode is enabled.

---

## Phase 6 — Follow-up Agent + Loop Closure
**Deliverable:** Agent 6 running, replies handled, demos booked in HubSpot

### What gets built
- Reply poller — checks Apollo (email replies) + HeyReach (LinkedIn replies) for responses
- Reply classifier — positive / negative / neutral / out-of-office
- Escalation logic — positive reply → creates HubSpot task assigned to Rob
- Demo booking logger — marks Account status = meeting_booked in HubSpot
- Sequence pause logic — reply received → pause remaining sequence steps
- 90-day requeue — no reply after Day 30 → mark dormant, requeue after 90 days

### Test Criteria
```
✓ Positive reply → sequence paused, HubSpot task created for Rob
✓ Negative reply / opt-out → sequence stopped, contact permanently blocked
✓ Out-of-office reply → sequence paused, resumes after OOO date
✓ Demo booked → Account.status = meeting_booked, logged in HubSpot
✓ No reply after Day 30 → Account.status = dormant, requeues after 90 days
✓ 90-day dedup: dormant account not re-researched until 90 days elapsed
✓ All reply events written to Outreach table with updated status
```

### Demo
Simulate a positive reply from a test contact. Xavier sees HubSpot task appear for Rob with full context (company, contact, which message they replied to, suggested next step). Account status updates to meeting_booked after demo is confirmed.

---

## Phase 7 — Full Pipeline Run + Quality Gates
**Deliverable:** End-to-end run processing 10 real accounts, all quality gates passing

### What gets built
- Orchestrator — runs all 6 agents in sequence for each account
- Weekly run scheduler — kicks off every Monday morning
- Anti-pattern agent — scans codebase for structural issues, security vulnerabilities, N+1 queries
- Full test suite — all Phase 1–6 tests run together, zero failures
- Run summary report — Slack message to Xavier after each weekly run: accounts processed, contacts enrolled, demos booked

### Test Criteria
```
✓ Anti-pattern agent: zero structural issues flagged
✓ Linter: zero errors
✓ Full test suite: all Phase 1–6 tests pass
✓ 10-account end-to-end run completes without errors
✓ No excluded account ever reaches outreach
✓ No contact below Director level enrolled
✓ No contact re-enrolled within 90 days
✓ Weekly run summary fires to Slack after completion
✓ All activity visible in HubSpot
```

### Demo
Live run on 10 real net-new accounts. Xavier sees the full output: accounts discovered, scored, contacts found, sequences enrolled, and a Slack summary. Rob can see activity in HubSpot. Zero manual intervention required.

---

## Phase Summary

| Phase | What It Proves | Est. Complexity |
|---|---|---|
| 1 | Foundation works, exclusion list is airtight | Low |
| 2 | System can find and qualify real companies | Medium |
| 3 | Signal scoring + notification fires correctly | Medium |
| 4 | Right people found, right persona labels | Medium |
| 5 | Outreach sends correctly per persona + sequence | High |
| 6 | Replies handled, demos close the loop | High |
| 7 | Full pipeline runs cleanly, production-ready | Medium |

---

## Definition of Done (Full System)

- [ ] 50 net-new accounts researched per weekly run
- [ ] Zero excluded accounts ever contacted
- [ ] Zero contacts below Director level enrolled
- [ ] 90-day deduplication enforced on all contacts and accounts
- [ ] All outreach in Rob's voice using approved templates
- [ ] 70+ quality score accounts notify Xavier via Slack within 1 hour of detection
- [ ] Positive replies create HubSpot tasks for Rob within 15 minutes
- [ ] Booked demos logged in HubSpot automatically
- [ ] Full test suite passes with zero failures
- [ ] Anti-pattern agent finds zero issues
