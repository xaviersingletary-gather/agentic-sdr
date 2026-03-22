# Phase 2: Prospector Agent + ICP Qualifier Agent

## Context

You are building Phase 2 of Rob's Agentic SDR — a fully autonomous outbound sales system for Gather AI.

The project lives at: `/Users/xavier.singletary/Robs Agentic SDR/agentic-sdr/`

Phase 1 (scaffold) is complete:
- SQLAlchemy models: Account, Contact, Signal, Outreach
- Exclusion engine with fuzzy matching (src/exclusions/checker.py)
- Client stubs: Clay, Exa, Apollo, HeyReach, HubSpot, Slack (all raise NotImplementedError)
- 18/18 Phase 1 tests passing

## Your Task

Implement `src/agents/prospector.py` and `src/agents/icp_qualifier.py` so that ALL tests in `tests/test_prospector.py` pass.

## ICP Scoring Rubric (implement exactly as specified)

| Dimension | Criteria | Points |
|---|---|---|
| Revenue | $500M–$1B | 15 |
| Revenue | $1B+ | 25 |
| Facilities | 11–24 | 15 |
| Facilities | 25+ | 25 |
| Vertical | Exact ICP match (Logistics, Food_Bev, Healthcare_Pharma, Retail, Manufacturing, CPG) | 20 |
| Vertical | Adjacent (other) | 0 |
| WMS detected | True | 15 |
| Automation footprint | True | 15 |
| **Max total** | | **100** |

Pass threshold: **≥ 40**. Below 40 = disqualified.

## ProspectorAgent Requirements

```python
class ProspectorAgent:
    def __init__(self, db, exa_client, clay_client):
        ...

    def run(self) -> list[Account]:
        # 1. Use exa_client.search() with ICP-targeted queries
        # 2. For each result, call clay_client.get_company(domain)
        # 3. Check exclusion list — skip if excluded
        # 4. Skip if revenue < $500M
        # 5. Skip if duplicate domain already in DB
        # 6. Save Account to DB with status=researching
        # 7. Return list of saved Account objects
```

## ICPQualifierAgent Requirements

```python
class ICPQualifierAgent:
    def __init__(self, db):
        ...

    def score(self, account: Account) -> dict:
        # Returns: {
        #   "icp_score": float (0-100),
        #   "pass": bool,
        #   "score_breakdown": {
        #       "revenue": int,
        #       "facilities": int,
        #       "vertical": int,
        #       "wms": int,
        #       "automation": int
        #   },
        #   "disqualification_reason": str | None
        # }
        # Side effects:
        #   - Updates account.icp_score
        #   - Updates account.status = "qualified" or "disqualified"
        #   - Updates account.disqualification_reason if disqualified
        #   - Commits to DB
```

## ICP Verticals (exact match list)

```python
ICP_VERTICALS = ["Logistics", "Food_Bev", "Healthcare_Pharma", "Retail", "Manufacturing", "CPG"]
```

## Steps to Complete

1. Read the existing codebase to understand the models and structure
2. Implement `src/agents/prospector.py`
3. Implement `src/agents/icp_qualifier.py`
4. Run `cd "/Users/xavier.singletary/Robs Agentic SDR/agentic-sdr" && python3 -m pytest tests/test_prospector.py -v` from the project directory
5. Fix any failures
6. Confirm ALL Phase 1 tests still pass: `python3 -m pytest tests/ -v`
7. When all tests pass, output exactly: <promise>PHASE_2_COMPLETE</promise>

## Rules

- Do NOT modify any test files
- Do NOT modify Phase 1 files (models, exclusions) unless fixing a genuine bug
- Use `src/config.py` for all config values
- All DB operations must use the passed `db` session
- Agents must work with mocked clients (tests inject mocks)
- Keep it simple — no Claude API calls needed in Phase 2, pure Python logic

## Current test run (should show 13 failures — your job is to make them pass)

```bash
cd "/Users/xavier.singletary/Robs Agentic SDR/agentic-sdr" && python3 -m pytest tests/test_prospector.py -v
```

Start by reading the test file, then read the existing models and exclusion checker, then implement.
