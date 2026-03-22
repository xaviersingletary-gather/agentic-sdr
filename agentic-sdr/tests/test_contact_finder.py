"""
Phase 4 Tests: Contact Finder Agent
"""
import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.base import Base
from src.models.account import Account, AccountStatus
from src.models.contact import Contact, PersonaType, OutreachStatus
from src.agents.contact_finder import ContactFinderAgent


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def qualified_account(db):
    account = Account(
        company_name="Summit 3PL", domain="summit3pl.com",
        industry="Logistics", annual_revenue=800_000_000,
        facility_count=15, icp_score=75.0,
        status=AccountStatus.qualified
    )
    db.add(account)
    db.commit()
    return account


class TestContactFinderAgent:

    def test_finds_and_saves_contacts(self, db, qualified_account):
        """ContactFinder saves at least one contact for a qualified account."""
        mock_apollo = MagicMock()
        mock_apollo.search_people.return_value = [
            {"first_name": "Jane", "last_name": "Doe",
             "title": "Director of Continuous Improvement",
             "email": "jane.doe@summit3pl.com", "phone": "555-1234",
             "linkedin_url": "https://linkedin.com/in/janedoe"}
        ]

        agent = ContactFinderAgent(db=db, apollo_client=mock_apollo)
        contacts = agent.find(qualified_account)

        assert len(contacts) >= 1
        assert db.query(Contact).filter_by(account_id=qualified_account.id).count() >= 1

    def test_assigns_tdm_persona_to_ops_director(self, db, qualified_account):
        """Director/VP of Operations/Continuous Improvement mapped to TDM persona."""
        mock_apollo = MagicMock()
        mock_apollo.search_people.return_value = [
            {"first_name": "Jane", "last_name": "Doe",
             "title": "VP of Warehouse Operations",
             "email": "jane@summit3pl.com", "phone": None,
             "linkedin_url": "https://linkedin.com/in/janedoe"}
        ]

        agent = ContactFinderAgent(db=db, apollo_client=mock_apollo)
        contacts = agent.find(qualified_account)

        assert contacts[0].persona_type == PersonaType.tdm

    def test_assigns_financial_sponsor_to_cfo(self, db, qualified_account):
        """CFO/VP Finance mapped to Financial_Sponsor persona."""
        mock_apollo = MagicMock()
        mock_apollo.search_people.return_value = [
            {"first_name": "Bob", "last_name": "Smith",
             "title": "CFO",
             "email": "bob@summit3pl.com", "phone": None,
             "linkedin_url": "https://linkedin.com/in/bobsmith"}
        ]

        agent = ContactFinderAgent(db=db, apollo_client=mock_apollo)
        contacts = agent.find(qualified_account)

        assert contacts[0].persona_type == PersonaType.financial_sponsor

    def test_filters_out_below_director_level(self, db, qualified_account):
        """Contacts below Director level are not saved."""
        mock_apollo = MagicMock()
        mock_apollo.search_people.return_value = [
            {"first_name": "Tim", "last_name": "Jones",
             "title": "Warehouse Associate",
             "email": "tim@summit3pl.com", "phone": None,
             "linkedin_url": "https://linkedin.com/in/timjones"},
            {"first_name": "Sara", "last_name": "Lee",
             "title": "Director of Supply Chain",
             "email": "sara@summit3pl.com", "phone": None,
             "linkedin_url": "https://linkedin.com/in/saralee"}
        ]

        agent = ContactFinderAgent(db=db, apollo_client=mock_apollo)
        contacts = agent.find(qualified_account)

        assert len(contacts) == 1
        assert contacts[0].first_name == "Sara"

    def test_deduplication_skips_existing_contacts(self, db, qualified_account):
        """Does not create duplicate contact records for the same email."""
        existing = Contact(
            account_id=qualified_account.id,
            first_name="Jane", last_name="Doe",
            email="jane@summit3pl.com"
        )
        db.add(existing)
        db.commit()

        mock_apollo = MagicMock()
        mock_apollo.search_people.return_value = [
            {"first_name": "Jane", "last_name": "Doe",
             "title": "Director of Ops",
             "email": "jane@summit3pl.com", "phone": None,
             "linkedin_url": "https://linkedin.com/in/janedoe"}
        ]

        agent = ContactFinderAgent(db=db, apollo_client=mock_apollo)
        agent.find(qualified_account)

        assert db.query(Contact).filter_by(email="jane@summit3pl.com").count() == 1

    def test_tdm_persona_returned_first(self, db, qualified_account):
        """TDM persona contact is prioritized first in returned list."""
        mock_apollo = MagicMock()
        mock_apollo.search_people.return_value = [
            {"first_name": "Bob", "last_name": "CFO",
             "title": "CFO", "email": "bob@summit3pl.com",
             "phone": None, "linkedin_url": "https://linkedin.com/in/bob"},
            {"first_name": "Jane", "last_name": "Ops",
             "title": "VP of Warehouse Operations",
             "email": "jane@summit3pl.com", "phone": None,
             "linkedin_url": "https://linkedin.com/in/jane"}
        ]

        agent = ContactFinderAgent(db=db, apollo_client=mock_apollo)
        contacts = agent.find(qualified_account)

        tdm_contacts = [c for c in contacts if c.persona_type == PersonaType.tdm]
        assert len(tdm_contacts) >= 1
        assert contacts[0].persona_type == PersonaType.tdm

    def test_contact_status_set_to_pending(self, db, qualified_account):
        """New contacts saved with outreach_status = pending."""
        mock_apollo = MagicMock()
        mock_apollo.search_people.return_value = [
            {"first_name": "Jane", "last_name": "Doe",
             "title": "Director of Ops", "email": "jane@summit3pl.com",
             "phone": None, "linkedin_url": "https://linkedin.com/in/jane"}
        ]

        agent = ContactFinderAgent(db=db, apollo_client=mock_apollo)
        contacts = agent.find(qualified_account)

        assert all(c.outreach_status == OutreachStatus.pending for c in contacts)

    def test_returns_empty_list_when_no_contacts_found(self, db, qualified_account):
        """Returns empty list when Apollo returns no results."""
        mock_apollo = MagicMock()
        mock_apollo.search_people.return_value = []

        agent = ContactFinderAgent(db=db, apollo_client=mock_apollo)
        contacts = agent.find(qualified_account)

        assert contacts == []
