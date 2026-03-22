from datetime import datetime, timezone
from src.models.account import Account, AccountStatus
from src.models.contact import Contact, OutreachStatus
from src.models.outreach import Outreach, Channel, OutreachStatus as OutreachRecordStatus

HEYREACH_CAMPAIGN_ID = "default_campaign"


class OutreachAgent:
    def __init__(self, db, apollo_client, heyreach_client, hubspot_client,
                 templates: dict, dry_run: bool = True):
        self.db = db
        self.apollo = apollo_client
        self.heyreach = heyreach_client
        self.hubspot = hubspot_client
        self.templates = templates
        self.dry_run = dry_run

    def enroll(self, account: Account, contact: Contact) -> dict:
        # Skip if already enrolled
        if contact.outreach_status == OutreachStatus.enrolled:
            return {"skipped": True, "reason": "already_enrolled"}

        personalization = {
            "first_name": contact.first_name or "",
            "company_name": account.company_name,
            "persona_type": contact.persona_type or "tdm",
        }

        if not self.dry_run:
            # Enroll in Apollo email sequence
            self.apollo.create_sequence(
                contact_id=str(contact.id),
                sequence_id=f"{contact.persona_type}_sequence"
            )

            # Enroll in HeyReach LinkedIn campaign
            if contact.linkedin_url:
                self.heyreach.add_to_campaign(
                    campaign_id=HEYREACH_CAMPAIGN_ID,
                    linkedin_url=contact.linkedin_url,
                    personalization=personalization,
                )

            # Log to HubSpot
            self.hubspot.log_activity(
                contact_id=str(contact.id),
                note=f"Enrolled in SDR sequence. Account: {account.company_name}. "
                     f"Persona: {contact.persona_type}. Day 0 outreach initiated."
            )

        # Save outreach records
        outreach = Outreach(
            contact_id=contact.id,
            account_id=account.id,
            channel=Channel.email,
            sequence_day=0,
            template_id=f"{contact.persona_type}_day0_email",
            message_content=self.templates.get(f"{contact.persona_type}_day0_email", ""),
            status=OutreachRecordStatus.pending if self.dry_run else OutreachRecordStatus.sent,
            sent_at=None if self.dry_run else datetime.now(timezone.utc),
        )
        self.db.add(outreach)

        # Update statuses
        contact.outreach_status = OutreachStatus.enrolled
        account.status = AccountStatus.in_outreach
        self.db.commit()

        return {"enrolled": True, "dry_run": self.dry_run}
