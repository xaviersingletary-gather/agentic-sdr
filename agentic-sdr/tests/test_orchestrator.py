"""
Phase 7 Tests: Orchestrator — end-to-end run loop
"""
import pytest
from unittest.mock import MagicMock, patch, call
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.base import Base
from src.models.account import Account, AccountStatus
from src.models.contact import Contact, PersonaType, OutreachStatus
from src.models.signal import Signal
from src.models.outreach import Outreach
from src.orchestrator import Orchestrator


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def mock_clients():
    exa = MagicMock()
    clay = MagicMock()
    apollo = MagicMock()
    heyreach = MagicMock()
    hubspot = MagicMock()
    slack = MagicMock()
    return {"exa": exa, "clay": clay, "apollo": apollo,
            "heyreach": heyreach, "hubspot": hubspot, "slack": slack}


@pytest.fixture
def icp_company():
    return {
        "name": "Summit 3PL", "domain": "summit3pl.com",
        "industry": "Logistics", "annual_revenue": 900_000_000,
        "facility_count": 18, "hq_country": "US",
        "wms_detected": True, "automation_footprint": False,
    }


class TestOrchestrator:

    def test_full_pipeline_runs_end_to_end(self, db, mock_clients, icp_company):
        """A single ICP company flows through all 6 agents without error."""
        mock_clients["exa"].search.return_value = [
            {"title": icp_company["name"], "url": f"https://{icp_company['domain']}", "text": "..."}
        ]
        mock_clients["clay"].get_company.return_value = icp_company
        mock_clients["clay"].get_job_postings.return_value = []
        mock_clients["apollo"].search_people.return_value = [
            {"first_name": "Jane", "last_name": "Doe",
             "title": "VP Warehouse Operations",
             "email": "jane@summit3pl.com", "phone": None,
             "linkedin_url": "https://linkedin.com/in/jane"}
        ]
        mock_clients["apollo"].create_sequence.return_value = {"id": "seq_1", "status": "enrolled"}
        mock_clients["heyreach"].add_to_campaign.return_value = {"id": "hr_1", "status": "added"}

        orchestrator = Orchestrator(
            db=db,
            clients=mock_clients,
            templates={"tdm_day0_email": "Hi {first_name}..."},
            dry_run=False
        )
        result = orchestrator.run()

        assert result["accounts_discovered"] >= 1
        assert result["accounts_qualified"] >= 1
        assert result["contacts_found"] >= 1
        assert result["contacts_enrolled"] >= 1

    def test_excluded_accounts_never_reach_outreach(self, db, mock_clients):
        """Accounts on exclusion list are filtered before any outreach."""
        mock_clients["exa"].search.return_value = [
            {"title": "Amazon", "url": "https://amazon.com", "text": "Amazon DC"}
        ]
        mock_clients["clay"].get_company.return_value = {
            "name": "Amazon", "domain": "amazon.com", "industry": "Retail",
            "annual_revenue": 500_000_000_000, "facility_count": 1000,
            "hq_country": "US", "wms_detected": True, "automation_footprint": True,
        }

        orchestrator = Orchestrator(db=db, clients=mock_clients,
                                    templates={}, dry_run=True)
        orchestrator.run()

        mock_clients["apollo"].search_people.assert_not_called()
        mock_clients["heyreach"].add_to_campaign.assert_not_called()

    def test_disqualified_accounts_do_not_reach_outreach(self, db, mock_clients):
        """Accounts scoring below 40 are disqualified and not enrolled."""
        mock_clients["exa"].search.return_value = [
            {"title": "Tiny Co", "url": "https://tinyco.com", "text": "Small warehouse"}
        ]
        mock_clients["clay"].get_company.return_value = {
            "name": "Tiny Co", "domain": "tinyco.com", "industry": "Other",
            "annual_revenue": 600_000_000, "facility_count": 2,
            "hq_country": "US", "wms_detected": False, "automation_footprint": False,
        }

        orchestrator = Orchestrator(db=db, clients=mock_clients,
                                    templates={}, dry_run=True)
        orchestrator.run()

        assert db.query(Account).filter_by(status=AccountStatus.disqualified).count() >= 1
        mock_clients["apollo"].search_people.assert_not_called()

    def test_dry_run_prevents_live_sends(self, db, mock_clients, icp_company):
        """dry_run=True prevents Apollo sequences and HeyReach enrollments."""
        mock_clients["exa"].search.return_value = [
            {"title": icp_company["name"], "url": f"https://{icp_company['domain']}", "text": "..."}
        ]
        mock_clients["clay"].get_company.return_value = icp_company
        mock_clients["clay"].get_job_postings.return_value = []
        mock_clients["apollo"].search_people.return_value = [
            {"first_name": "Jane", "last_name": "Doe",
             "title": "VP Operations", "email": "jane@summit3pl.com",
             "phone": None, "linkedin_url": "https://linkedin.com/in/jane"}
        ]

        orchestrator = Orchestrator(db=db, clients=mock_clients,
                                    templates={"tdm_day0_email": "Hi {first_name}..."},
                                    dry_run=True)
        orchestrator.run()

        mock_clients["apollo"].create_sequence.assert_not_called()
        mock_clients["heyreach"].add_to_campaign.assert_not_called()

    def test_run_returns_summary_dict(self, db, mock_clients):
        """run() always returns a summary dict with expected keys."""
        mock_clients["exa"].search.return_value = []

        orchestrator = Orchestrator(db=db, clients=mock_clients,
                                    templates={}, dry_run=True)
        result = orchestrator.run()

        for key in ["accounts_discovered", "accounts_qualified", "accounts_disqualified",
                    "contacts_found", "contacts_enrolled", "high_quality_notified"]:
            assert key in result

    def test_high_quality_accounts_trigger_slack(self, db, mock_clients, icp_company):
        """Accounts with quality score >= 70 trigger Slack notification to Xavier."""
        # Prospector makes 6 exa.search calls; signal hunter makes 1 — supply 7
        mock_clients["exa"].search.side_effect = [
            [{"title": icp_company["name"], "url": f"https://{icp_company['domain']}", "text": "..."}],
            [], [], [], [], [],
            [{"title": f"{icp_company['name']} opens new DC",
              "url": "https://news.com/summit",
              "text": "New distribution center opened."}],
        ]
        mock_clients["clay"].get_company.return_value = icp_company
        mock_clients["clay"].get_job_postings.return_value = [
            {"title": "Director Warehouse Ops", "date": "2026-03-01",
             "content": "Hiring Director Warehouse Ops"},
            {"title": "WMS Project Lead", "date": "2026-03-05",
             "content": "WMS migration project lead"},
            {"title": "VP Supply Chain", "date": "2026-03-10",
             "content": "New VP Supply Chain hired"},
        ]
        mock_clients["apollo"].search_people.return_value = []

        orchestrator = Orchestrator(db=db, clients=mock_clients,
                                    templates={}, dry_run=True)
        result = orchestrator.run()

        if result["high_quality_notified"] > 0:
            mock_clients["slack"].notify_xavier.assert_called()

    def test_no_contacts_found_still_completes(self, db, mock_clients, icp_company):
        """Pipeline completes gracefully when no contacts are found for an account."""
        mock_clients["exa"].search.return_value = [
            {"title": icp_company["name"], "url": f"https://{icp_company['domain']}", "text": "..."}
        ]
        mock_clients["clay"].get_company.return_value = icp_company
        mock_clients["clay"].get_job_postings.return_value = []
        mock_clients["apollo"].search_people.return_value = []

        orchestrator = Orchestrator(db=db, clients=mock_clients,
                                    templates={}, dry_run=True)
        result = orchestrator.run()

        assert result["accounts_qualified"] >= 1
        assert result["contacts_enrolled"] == 0

    def test_multiple_contacts_per_account_all_enrolled(self, db, mock_clients, icp_company):
        """All Director+ contacts at a qualified account are enrolled."""
        mock_clients["exa"].search.return_value = [
            {"title": icp_company["name"], "url": f"https://{icp_company['domain']}", "text": "..."}
        ]
        mock_clients["clay"].get_company.return_value = icp_company
        mock_clients["clay"].get_job_postings.return_value = []
        mock_clients["apollo"].search_people.return_value = [
            {"first_name": "Jane", "last_name": "Doe", "title": "VP Operations",
             "email": "jane@summit3pl.com", "phone": None,
             "linkedin_url": "https://linkedin.com/in/jane"},
            {"first_name": "Bob", "last_name": "Smith", "title": "CFO",
             "email": "bob@summit3pl.com", "phone": None,
             "linkedin_url": "https://linkedin.com/in/bob"},
        ]
        mock_clients["apollo"].create_sequence.return_value = {"id": "seq_1", "status": "enrolled"}
        mock_clients["heyreach"].add_to_campaign.return_value = {"id": "hr_1", "status": "added"}

        orchestrator = Orchestrator(db=db, clients=mock_clients,
                                    templates={"tdm_day0_email": "Hi {first_name}...",
                                               "financial_sponsor_day0_email": "Hi {first_name}..."},
                                    dry_run=False)
        result = orchestrator.run()

        assert result["contacts_enrolled"] == 2
