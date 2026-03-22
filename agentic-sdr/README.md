# Rob's Agentic SDR

A fully autonomous sales development system that hunts, qualifies, and sequences net-new prospects — from scratch — so Rob can focus on closing.

---

## What It Does

1. **Discovers** ICP-fit companies using Exa (web search) + Clay (enrichment)
2. **Qualifies** each account against Gather AI's ICP criteria (500M+ revenue, 11+ facilities, target verticals)
3. **Hunts for signals** — job postings, new DCs, WMS migrations, audit failures, automation adoption
4. **Finds contacts** at Director+ level via Apollo + LinkedIn Sales Navigator
5. **Sequences automatically** — LinkedIn (HeyReach) + email (Apollo) across Days 0, 3, 7, 14, 30
6. **Notifies Xavier** via Slack when an account scores 70+
7. **Logs everything** to HubSpot as the system of record
8. **Finish line:** booked demo handed off to Rob

---

## Architecture

```
src/
├── agents/
│   ├── prospector.py        # Exa + Clay → candidate companies
│   ├── icp_qualifier.py     # Scores company 0-100 against ICP
│   ├── signal_hunter.py     # Detects buying signals, triggers Xavier notification
│   ├── contact_finder.py    # Apollo + Sales Nav → verified contacts
│   ├── outreach_agent.py    # Enrolls in HeyReach (LinkedIn) + Apollo (email)
│   └── follow_up_agent.py   # Monitors replies, books demo, updates HubSpot
├── clients/
│   ├── clay.py              # Clay API wrapper
│   ├── exa.py               # Exa API wrapper
│   ├── apollo.py            # Apollo people search + sequence enrollment
│   ├── heyreach.py          # HeyReach LinkedIn campaign enrollment
│   ├── hubspot.py           # HubSpot CRM logging + task creation
│   └── slack.py             # Xavier's personal Slack notifications
├── models/
│   ├── account.py           # Company + ICP/quality scores + status
│   ├── contact.py           # Contact + persona type + outreach status
│   ├── signal.py            # Buying signals + points mapping
│   └── outreach.py          # Sequence log per contact
├── exclusions/
│   ├── lists.py             # Hardcoded customers, target, strategic accounts
│   └── checker.py           # Fuzzy match exclusion gate (token_set_ratio, threshold 88)
└── config.py                # Env vars + feature flags
```

---

## Tool Stack

| Function | Tool |
|---|---|
| Company discovery | Exa + Clay |
| Contact finding | Apollo + LinkedIn Sales Navigator |
| Email sequences | Apollo (Rob's connected mailbox) |
| LinkedIn sequences | HeyReach |
| CRM / system of record | HubSpot |
| Quality notifications | Slack (Xavier's personal channel) |
| Agent intelligence | Anthropic Claude (claude-3-5-sonnet) |

---

## Outreach Sequence

| Day | Channel | Action |
|---|---|---|
| 0 | LinkedIn + Email | Connection request + intro email |
| 3 | LinkedIn | Follow-up message (if connected) |
| 7 | Email + Phone flag | Follow-up email + Rob notified to call |
| 14 | Email | Value-add touchpoint |
| 30 | Email | Break-up message |

---

## Exclusion Rules

The system **will not contact** any account on the following lists:
- **Customers** — active Gather AI customers
- **Target Accounts** — named strategic pursuit list
- **Strategic Accounts** — highest-priority named accounts

Exclusion uses fuzzy matching (`token_set_ratio`, threshold 88) so variants like `"Amazon Logistics"`, `"Geodis NA"`, and `"P&G"` are also blocked.

---

## ICP Criteria (Qualification Floor)

| Dimension | Minimum |
|---|---|
| Annual revenue | $500M+ |
| Facilities | 11+ warehouse/DC locations |
| Verticals | 3PL, Food & Bev, Retail, Pharma, Manufacturing, CPG |
| Contact seniority | Director+ |
| Re-contact window | 90-day deduplication |

Accounts scoring **below 40** are disqualified. Accounts scoring **70+** trigger a Slack notification to Xavier.

---

## Setup

### 1. Clone & install
```bash
git clone https://github.com/xaviersingletary-gather/agentic-sdr.git
cd agentic-sdr
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Fill in all API keys in .env
```

### 3. Initialize the database
```bash
python3 -c "from src.models.base import init_db; init_db()"
```

### 4. Run tests
```bash
pytest
```

### 5. Run the SDR (dry run — no live sends)
```bash
DRY_RUN=true python3 -m src.orchestrator
```

### 6. Go live
```bash
# Set DRY_RUN=false in .env when ready
python3 -m src.orchestrator
```

---

## Required API Keys

| Key | Where to get it |
|---|---|
| `ANTHROPIC_API_KEY` | console.anthropic.com |
| `CLAY_API_KEY` | app.clay.com → Settings → API |
| `EXA_API_KEY` | exa.ai → Dashboard |
| `APOLLO_API_KEY` | app.apollo.io → Settings → Integrations |
| `APOLLO_EMAIL_ACCOUNT_ID` | Apollo → Email Accounts → Rob's mailbox ID |
| `HEYREACH_API_KEY` | app.heyreach.io → API |
| `HUBSPOT_ACCESS_TOKEN` | HubSpot → Settings → Private Apps |
| `SLACK_BOT_TOKEN` | api.slack.com → Your Apps |
| `SLACK_XAVIER_CHANNEL_ID` | Xavier's personal Slack channel ID |

---

## Build Phases

| Phase | Status | What's built |
|---|---|---|
| 1 — Scaffold | ✅ Done | Data models, exclusion engine, client stubs, test suite |
| 2 — Prospector | 🔜 Next | Exa + Clay discovery + ICP qualifier (agents 1 & 2) |
| 3 — Signal Hunter | ⬜ | Buying signal detection + Xavier Slack notification (agent 3) |
| 4 — Contact Finder | ⬜ | Apollo + Sales Nav contact enrichment (agent 4) |
| 5 — Outreach | ⬜ | HeyReach + Apollo sequence enrollment (agent 5) |
| 6 — Follow-up | ⬜ | Reply monitoring + demo booking + HubSpot sync (agent 6) |
| 7 — Orchestrator | ⬜ | End-to-end run loop with scheduling |

---

## Key Decisions

- **Fully autonomous after template approval** — Xavier approves templates + strategy once; the system runs without per-prospect approval
- **Rob is the sender persona** — all outreach goes from Rob's identity (email + LinkedIn)
- **DRY_RUN=true by default** — nothing sends until explicitly enabled
- **No EMEA-only accounts**
- **No contacts below Director level**
- **90-day deduplication** — same person not contacted within 90 days
- **No post-demo follow-up** — handoff to Rob at meeting booked; AE owns from there

---

*Built by Xavier Singletary, Go-to-Market Engineer @ Gather AI*
