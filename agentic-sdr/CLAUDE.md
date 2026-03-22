# Agentic SDR — Claude Project Context

## What This Is
Rob's fully autonomous SDR system for Gather AI. Hunts, qualifies, and sequences net-new prospects. Rob is the sender persona. Xavier is the GTM engineer/builder.

## Project Root
`/Users/xavier.singletary/Robs Agentic SDR/agentic-sdr/`

## Run Tests
```bash
cd "/Users/xavier.singletary/Robs Agentic SDR/agentic-sdr"
python3 -m pytest tests/ -v
```

## Key Rules
1. DRY_RUN=true by default — never send live outreach without explicit flag
2. ALWAYS check exclusion list before processing any account
3. Never contact: customers, target accounts, strategic accounts
4. Never contact below Director level
5. 90-day deduplication on contacts
6. All DB operations use the passed `db` session — never create new sessions in agents
7. Never modify test files

## ICP Score Thresholds
- < 40 = disqualify
- 40–69 = qualify → outreach
- 70+ = qualify → outreach + notify Xavier via Slack

## Tool Stack
- Discovery: Exa + Clay
- Contacts: Apollo + Sales Navigator
- LinkedIn: HeyReach
- Email: Apollo sequences
- CRM: HubSpot
- Notifications: Slack (Xavier's personal channel)
- AI: Anthropic Claude (claude-3-5-sonnet-20241022)

## Build Phases
- Phase 1 ✅ Scaffold (models, exclusions, client stubs)
- Phase 2 🔜 Prospector + ICP Qualifier
- Phase 3 ⬜ Signal Hunter + Slack notification
- Phase 4 ⬜ Contact Finder
- Phase 5 ⬜ Outreach (HeyReach + Apollo)
- Phase 6 ⬜ Follow-up + HubSpot sync
- Phase 7 ⬜ Orchestrator + scheduling
