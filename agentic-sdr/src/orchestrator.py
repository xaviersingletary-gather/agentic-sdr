"""
Orchestrator — ties all 6 agents into a single run loop.

Pipeline per run:
  1. Prospector      → discover candidate companies
  2. ICPQualifier    → score and qualify/disqualify each
  3. SignalHunter    → find buying signals, notify Xavier if score >= 70
  4. ContactFinder   → find Director+ contacts at qualified accounts
  5. OutreachAgent   → enroll contacts in LinkedIn + email sequences
  6. FollowUpAgent   → handles replies (called externally via webhook/poll)
"""
import logging
from datetime import datetime, timezone

from src.agents.prospector import ProspectorAgent
from src.agents.icp_qualifier import ICPQualifierAgent
from src.agents.signal_hunter import SignalHunterAgent
from src.agents.contact_finder import ContactFinderAgent
from src.agents.outreach_agent import OutreachAgent
from src.agents.follow_up_agent import FollowUpAgent
from src.models.account import AccountStatus
from src.config import DRY_RUN

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, db, clients: dict, templates: dict, dry_run: bool = True):
        self.db = db
        self.dry_run = dry_run

        # Instantiate all agents
        self.prospector = ProspectorAgent(
            db=db,
            exa_client=clients["exa"],
            clay_client=clients["clay"],
        )
        self.qualifier = ICPQualifierAgent(db=db)
        self.signal_hunter = SignalHunterAgent(
            db=db,
            clay_client=clients["clay"],
            exa_client=clients["exa"],
            slack_client=clients["slack"],
        )
        self.contact_finder = ContactFinderAgent(
            db=db,
            apollo_client=clients["apollo"],
        )
        self.outreach_agent = OutreachAgent(
            db=db,
            apollo_client=clients["apollo"],
            heyreach_client=clients["heyreach"],
            hubspot_client=clients["hubspot"],
            templates=templates,
            dry_run=dry_run,
        )
        self.follow_up_agent = FollowUpAgent(
            db=db,
            hubspot_client=clients["hubspot"],
        )

    def run(self) -> dict:
        summary = {
            "run_at": datetime.now(timezone.utc).isoformat(),
            "dry_run": self.dry_run,
            "accounts_discovered": 0,
            "accounts_qualified": 0,
            "accounts_disqualified": 0,
            "contacts_found": 0,
            "contacts_enrolled": 0,
            "high_quality_notified": 0,
        }

        # ── Step 1: Prospect ──────────────────────────────────────────────
        logger.info("Step 1: Prospecting...")
        candidates = self.prospector.run()
        summary["accounts_discovered"] = len(candidates)
        logger.info(f"  → {len(candidates)} candidate accounts found")

        for account in candidates:
            # ── Step 2: Qualify ───────────────────────────────────────────
            score_result = self.qualifier.score(account)
            self.db.refresh(account)

            if not score_result["pass"]:
                summary["accounts_disqualified"] += 1
                logger.info(f"  ✗ {account.company_name} disqualified (score={score_result['icp_score']:.0f})")
                continue

            summary["accounts_qualified"] += 1
            logger.info(f"  ✓ {account.company_name} qualified (score={score_result['icp_score']:.0f})")

            # ── Step 3: Signal Hunt ───────────────────────────────────────
            signal_result = self.signal_hunter.hunt(account)
            if signal_result["quality_score"] >= 70:
                summary["high_quality_notified"] += 1
                logger.info(f"  🔔 Xavier notified — quality score {signal_result['quality_score']:.0f}")

            # ── Step 4: Find Contacts ─────────────────────────────────────
            contacts = self.contact_finder.find(account)
            summary["contacts_found"] += len(contacts)
            logger.info(f"  → {len(contacts)} contacts found at {account.company_name}")

            if not contacts:
                continue

            # ── Step 5: Enroll in Outreach ────────────────────────────────
            for contact in contacts:
                result = self.outreach_agent.enroll(account, contact)
                if result.get("enrolled"):
                    summary["contacts_enrolled"] += 1

            logger.info(f"  📧 {summary['contacts_enrolled']} contact(s) enrolled at {account.company_name}")

        logger.info(f"Run complete: {summary}")
        return summary
