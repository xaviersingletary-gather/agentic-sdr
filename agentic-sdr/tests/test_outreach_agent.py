"""
Phase 5 Tests: Outreach Agent
"""
import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.base import Base
from src.models.account import Account, AccountStatus
from src.models.contact import Contact, PersonaType, OutreachStatus
from src.models.outreach import Outreach, Channel, OutreachStatus as OutreachRecordStatus
from src.agents.outreach_agent import OutreachAgent


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def account_with_contact(db):
    account = Account(
        company_name="Summit 3PL", domain="summit3pl.com",
        industry="Logistics", annual_revenue=800_000_000,
        facility_count=15, icp_score=75.0,
        status=AccountStatus.qualified
    )
    db.add(account)
    db.commit()

    contact = Contact(
        account_id=account.id, first_name="Jane", last_name="Doe",
        title="Director of Warehouse Operations",
        persona_type=PersonaType.tdm,
        email="jane.doe@summit3pl.com",
        linkedin_url="https://linkedin.com/in/janedoe",
        verified=True, outreach_status=OutreachStatus.pending
    )
    db.add(contact)
    db.commit()
    return account, contact


MOCK_TEMPLATES = {
    "tdm_day0_email": "Hi {first_name}, I wanted to reach out about Gather AI...",
    "tdm_day0_linkedin": "Hi {first_name}, noticed Summit 3PL is expanding...",
}


class TestOutreachAgent:

    def test_enrolls_contact_in_email_sequence(self, db, account_with_contact):
        """Outreach agent enrolls contact in Apollo email sequence."""
        account, contact = account_with_contact
        mock_apollo = MagicMock()
        mock_apollo.create_sequence.return_value = {"id": "seq_123", "status": "enrolled"}
        mock_heyreach = MagicMock()
        mock_heyreach.add_to_campaign.return_value = {"id": "hr_123", "status": "added"}
        mock_hubspot = MagicMock()

        agent = OutreachAgent(db=db, apollo_client=mock_apollo,
                              heyreach_client=mock_heyreach,
                              hubspot_client=mock_hubspot,
                              templates=MOCK_TEMPLATES,
                              dry_run=False)
        agent.enroll(account, contact)

        mock_apollo.create_sequence.assert_called_once()

    def test_enrolls_contact_in_linkedin_campaign(self, db, account_with_contact):
        """Outreach agent adds contact to HeyReach LinkedIn campaign."""
        account, contact = account_with_contact
        mock_apollo = MagicMock()
        mock_apollo.create_sequence.return_value = {"id": "seq_123", "status": "enrolled"}
        mock_heyreach = MagicMock()
        mock_heyreach.add_to_campaign.return_value = {"id": "hr_123", "status": "added"}
        mock_hubspot = MagicMock()

        agent = OutreachAgent(db=db, apollo_client=mock_apollo,
                              heyreach_client=mock_heyreach,
                              hubspot_client=mock_hubspot,
                              templates=MOCK_TEMPLATES,
                              dry_run=False)
        agent.enroll(account, contact)

        mock_heyreach.add_to_campaign.assert_called_once()

    def test_outreach_record_saved_to_db(self, db, account_with_contact):
        """Outreach enrollment creates Outreach records in DB."""
        account, contact = account_with_contact
        mock_apollo = MagicMock()
        mock_apollo.create_sequence.return_value = {"id": "seq_123", "status": "enrolled"}
        mock_heyreach = MagicMock()
        mock_heyreach.add_to_campaign.return_value = {"id": "hr_123", "status": "added"}
        mock_hubspot = MagicMock()

        agent = OutreachAgent(db=db, apollo_client=mock_apollo,
                              heyreach_client=mock_heyreach,
                              hubspot_client=mock_hubspot,
                              templates=MOCK_TEMPLATES,
                              dry_run=False)
        agent.enroll(account, contact)

        records = db.query(Outreach).filter_by(contact_id=contact.id).all()
        assert len(records) >= 1

    def test_contact_status_updated_to_enrolled(self, db, account_with_contact):
        """Contact outreach_status is updated to enrolled after enrollment."""
        account, contact = account_with_contact
        mock_apollo = MagicMock()
        mock_apollo.create_sequence.return_value = {"id": "seq_123", "status": "enrolled"}
        mock_heyreach = MagicMock()
        mock_heyreach.add_to_campaign.return_value = {"id": "hr_123", "status": "added"}
        mock_hubspot = MagicMock()

        agent = OutreachAgent(db=db, apollo_client=mock_apollo,
                              heyreach_client=mock_heyreach,
                              hubspot_client=mock_hubspot,
                              templates=MOCK_TEMPLATES,
                              dry_run=False)
        agent.enroll(account, contact)
        db.refresh(contact)

        assert contact.outreach_status == OutreachStatus.enrolled

    def test_account_status_updated_to_in_outreach(self, db, account_with_contact):
        """Account status is updated to in_outreach after first enrollment."""
        account, contact = account_with_contact
        mock_apollo = MagicMock()
        mock_apollo.create_sequence.return_value = {"id": "seq_123", "status": "enrolled"}
        mock_heyreach = MagicMock()
        mock_heyreach.add_to_campaign.return_value = {"id": "hr_123", "status": "added"}
        mock_hubspot = MagicMock()

        agent = OutreachAgent(db=db, apollo_client=mock_apollo,
                              heyreach_client=mock_heyreach,
                              hubspot_client=mock_hubspot,
                              templates=MOCK_TEMPLATES,
                              dry_run=False)
        agent.enroll(account, contact)
        db.refresh(account)

        assert account.status == AccountStatus.in_outreach

    def test_dry_run_does_not_call_apis(self, db, account_with_contact):
        """In dry_run mode, no external API calls are made."""
        account, contact = account_with_contact
        mock_apollo = MagicMock()
        mock_heyreach = MagicMock()
        mock_hubspot = MagicMock()

        agent = OutreachAgent(db=db, apollo_client=mock_apollo,
                              heyreach_client=mock_heyreach,
                              hubspot_client=mock_hubspot,
                              templates=MOCK_TEMPLATES,
                              dry_run=True)
        agent.enroll(account, contact)

        mock_apollo.create_sequence.assert_not_called()
        mock_heyreach.add_to_campaign.assert_not_called()

    def test_hubspot_activity_logged(self, db, account_with_contact):
        """HubSpot activity is logged after enrollment."""
        account, contact = account_with_contact
        mock_apollo = MagicMock()
        mock_apollo.create_sequence.return_value = {"id": "seq_123", "status": "enrolled"}
        mock_heyreach = MagicMock()
        mock_heyreach.add_to_campaign.return_value = {"id": "hr_123", "status": "added"}
        mock_hubspot = MagicMock()

        agent = OutreachAgent(db=db, apollo_client=mock_apollo,
                              heyreach_client=mock_heyreach,
                              hubspot_client=mock_hubspot,
                              templates=MOCK_TEMPLATES,
                              dry_run=False)
        agent.enroll(account, contact)

        mock_hubspot.log_activity.assert_called_once()

    def test_no_reenrollment_of_active_contact(self, db, account_with_contact):
        """Does not re-enroll a contact already in outreach."""
        account, contact = account_with_contact
        contact.outreach_status = OutreachStatus.enrolled
        db.commit()

        mock_apollo = MagicMock()
        mock_heyreach = MagicMock()
        mock_hubspot = MagicMock()

        agent = OutreachAgent(db=db, apollo_client=mock_apollo,
                              heyreach_client=mock_heyreach,
                              hubspot_client=mock_hubspot,
                              templates=MOCK_TEMPLATES,
                              dry_run=False)
        agent.enroll(account, contact)

        mock_apollo.create_sequence.assert_not_called()
        mock_heyreach.add_to_campaign.assert_not_called()
