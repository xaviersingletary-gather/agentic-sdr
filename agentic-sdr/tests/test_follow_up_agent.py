"""
Phase 6 Tests: Follow-Up Agent
"""
import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.base import Base
from src.models.account import Account, AccountStatus
from src.models.contact import Contact, PersonaType, OutreachStatus
from src.models.outreach import Outreach, Channel, OutreachStatus as OutreachRecordStatus
from src.agents.follow_up_agent import FollowUpAgent


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def enrolled_contact(db):
    account = Account(
        company_name="Summit 3PL", domain="summit3pl.com",
        industry="Logistics", annual_revenue=800_000_000,
        status=AccountStatus.in_outreach
    )
    db.add(account)
    db.commit()

    contact = Contact(
        account_id=account.id, first_name="Jane", last_name="Doe",
        title="Director of Ops", persona_type=PersonaType.tdm,
        email="jane@summit3pl.com",
        linkedin_url="https://linkedin.com/in/jane",
        outreach_status=OutreachStatus.enrolled
    )
    db.add(contact)
    db.commit()

    outreach = Outreach(
        contact_id=contact.id, account_id=account.id,
        channel=Channel.email, sequence_day=0,
        status=OutreachRecordStatus.sent
    )
    db.add(outreach)
    db.commit()

    return account, contact, outreach


class TestFollowUpAgent:

    def test_positive_reply_updates_contact_status(self, db, enrolled_contact):
        """A positive reply sets contact outreach_status to replied."""
        account, contact, outreach = enrolled_contact
        mock_hubspot = MagicMock()

        agent = FollowUpAgent(db=db, hubspot_client=mock_hubspot)
        agent.handle_reply(contact, reply_type="positive", reply_content="Yes, interested!")
        db.refresh(contact)

        assert contact.outreach_status == OutreachStatus.replied

    def test_positive_reply_updates_account_to_meeting_booked(self, db, enrolled_contact):
        """A positive reply moves account status toward meeting_booked."""
        account, contact, outreach = enrolled_contact
        mock_hubspot = MagicMock()

        agent = FollowUpAgent(db=db, hubspot_client=mock_hubspot)
        agent.handle_reply(contact, reply_type="positive", reply_content="Yes, let's connect!")
        db.refresh(account)

        assert account.status == AccountStatus.meeting_booked

    def test_positive_reply_creates_hubspot_task(self, db, enrolled_contact):
        """A positive reply creates a HubSpot follow-up task for Rob."""
        account, contact, outreach = enrolled_contact
        mock_hubspot = MagicMock()

        agent = FollowUpAgent(db=db, hubspot_client=mock_hubspot)
        agent.handle_reply(contact, reply_type="positive", reply_content="Interested!")

        mock_hubspot.create_task.assert_called_once()

    def test_negative_reply_marks_contact_opted_out(self, db, enrolled_contact):
        """An unsubscribe/negative reply marks the contact as opted_out."""
        account, contact, outreach = enrolled_contact
        mock_hubspot = MagicMock()

        agent = FollowUpAgent(db=db, hubspot_client=mock_hubspot)
        agent.handle_reply(contact, reply_type="negative", reply_content="Unsubscribe please")
        db.refresh(contact)

        assert contact.outreach_status == OutreachStatus.opted_out

    def test_bounced_email_marks_contact_bounced(self, db, enrolled_contact):
        """A bounced email marks the contact as bounced."""
        account, contact, outreach = enrolled_contact
        mock_hubspot = MagicMock()

        agent = FollowUpAgent(db=db, hubspot_client=mock_hubspot)
        agent.handle_reply(contact, reply_type="bounce", reply_content="")
        db.refresh(contact)

        assert contact.outreach_status == OutreachStatus.bounced

    def test_hubspot_updated_on_any_reply(self, db, enrolled_contact):
        """HubSpot contact status is updated for any reply type."""
        account, contact, outreach = enrolled_contact
        mock_hubspot = MagicMock()

        agent = FollowUpAgent(db=db, hubspot_client=mock_hubspot)
        agent.handle_reply(contact, reply_type="positive", reply_content="Interested!")

        mock_hubspot.update_contact_status.assert_called_once()

    def test_outreach_record_updated_on_reply(self, db, enrolled_contact):
        """The Outreach record status is updated to replied on positive reply."""
        account, contact, outreach = enrolled_contact
        mock_hubspot = MagicMock()

        agent = FollowUpAgent(db=db, hubspot_client=mock_hubspot)
        agent.handle_reply(contact, reply_type="positive", reply_content="Yes!")
        db.refresh(outreach)

        assert outreach.status == OutreachRecordStatus.replied
