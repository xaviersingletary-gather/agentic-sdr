from src.models.account import Account, AccountStatus
from src.models.contact import Contact, OutreachStatus
from src.models.outreach import Outreach, OutreachStatus as OutreachRecordStatus

REPLY_TYPE_MAP = {
    "positive": OutreachStatus.replied,
    "negative": OutreachStatus.opted_out,
    "bounce": OutreachStatus.bounced,
}


class FollowUpAgent:
    def __init__(self, db, hubspot_client):
        self.db = db
        self.hubspot = hubspot_client

    def handle_reply(self, contact: Contact, reply_type: str, reply_content: str) -> dict:
        new_status = REPLY_TYPE_MAP.get(reply_type, OutreachStatus.replied)
        contact.outreach_status = new_status

        # Update the most recent outreach record
        outreach = (
            self.db.query(Outreach)
            .filter_by(contact_id=contact.id)
            .order_by(Outreach.created_at.desc())
            .first()
        )
        if outreach:
            if reply_type == "positive":
                outreach.status = OutreachRecordStatus.replied
            elif reply_type == "bounce":
                outreach.status = OutreachRecordStatus.bounced

        # Update account status on positive reply
        account = self.db.query(Account).filter_by(id=contact.account_id).first()
        if reply_type == "positive" and account:
            account.status = AccountStatus.meeting_booked
            self.hubspot.create_task(
                contact_id=str(contact.id),
                subject=f"Positive reply from {contact.first_name} {contact.last_name} at {account.company_name}",
                body=reply_content,
                owner_id="rob",
            )

        # Always update HubSpot contact status
        self.hubspot.update_contact_status(
            contact_id=str(contact.id),
            status=new_status,
        )

        self.db.commit()

        return {
            "contact_id": contact.id,
            "reply_type": reply_type,
            "new_status": new_status,
        }
