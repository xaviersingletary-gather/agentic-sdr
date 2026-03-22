"""
Phase 2 Tests: Prospector + ICP Qualifier
All tests use mocked API clients — no real API calls.
"""
import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.base import Base
from src.models.account import Account, AccountStatus
from src.agents.prospector import ProspectorAgent
from src.agents.icp_qualifier import ICPQualifierAgent


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


# ---------------------------------------------------------------------------
# ProspectorAgent tests
# ---------------------------------------------------------------------------

class TestProspectorAgent:

    def test_returns_list_of_candidate_accounts(self, db):
        """Prospector returns at least one Account record saved to DB."""
        mock_exa = MagicMock()
        mock_exa.search.return_value = [
            {"title": "Acme Cold Storage", "url": "https://acmecold.com",
             "text": "Acme Cold Storage operates 18 warehouses across the US."}
        ]
        mock_clay = MagicMock()
        mock_clay.get_company.return_value = {
            "name": "Acme Cold Storage", "domain": "acmecold.com",
            "industry": "Logistics", "annual_revenue": 800_000_000,
            "facility_count": 18, "hq_country": "US",
            "wms_detected": True, "automation_footprint": False
        }

        agent = ProspectorAgent(db=db, exa_client=mock_exa, clay_client=mock_clay)
        results = agent.run()

        assert len(results) >= 1
        assert all(isinstance(r, Account) for r in results)
        assert db.query(Account).count() >= 1

    def test_excluded_accounts_are_not_saved(self, db):
        """Prospector skips accounts on the exclusion list."""
        mock_exa = MagicMock()
        mock_exa.search.return_value = [
            {"title": "Amazon", "url": "https://amazon.com", "text": "Amazon warehouse network."}
        ]
        mock_clay = MagicMock()
        mock_clay.get_company.return_value = {
            "name": "Amazon", "domain": "amazon.com",
            "industry": "Retail", "annual_revenue": 500_000_000_000,
            "facility_count": 1000, "hq_country": "US",
            "wms_detected": True, "automation_footprint": True
        }

        agent = ProspectorAgent(db=db, exa_client=mock_exa, clay_client=mock_clay)
        results = agent.run()

        assert len(results) == 0
        saved = db.query(Account).filter_by(company_name="Amazon").first()
        assert saved is None

    def test_deduplication_skips_existing_accounts(self, db):
        """Prospector does not create duplicate account records."""
        existing = Account(company_name="Acme Cold Storage", domain="acmecold.com")
        db.add(existing)
        db.commit()

        mock_exa = MagicMock()
        mock_exa.search.return_value = [
            {"title": "Acme Cold Storage", "url": "https://acmecold.com", "text": "..."}
        ]
        mock_clay = MagicMock()
        mock_clay.get_company.return_value = {
            "name": "Acme Cold Storage", "domain": "acmecold.com",
            "industry": "Logistics", "annual_revenue": 800_000_000,
            "facility_count": 18, "hq_country": "US",
            "wms_detected": True, "automation_footprint": False
        }

        agent = ProspectorAgent(db=db, exa_client=mock_exa, clay_client=mock_clay)
        agent.run()

        assert db.query(Account).filter_by(domain="acmecold.com").count() == 1

    def test_accounts_below_revenue_floor_are_excluded(self, db):
        """Accounts with revenue < $500M are not saved."""
        mock_exa = MagicMock()
        mock_exa.search.return_value = [
            {"title": "Tiny Warehouse Co", "url": "https://tiny.com", "text": "Small warehouse."}
        ]
        mock_clay = MagicMock()
        mock_clay.get_company.return_value = {
            "name": "Tiny Warehouse Co", "domain": "tiny.com",
            "industry": "Logistics", "annual_revenue": 50_000_000,
            "facility_count": 2, "hq_country": "US",
            "wms_detected": False, "automation_footprint": False
        }

        agent = ProspectorAgent(db=db, exa_client=mock_exa, clay_client=mock_clay)
        results = agent.run()

        assert len(results) == 0

    def test_multiple_candidates_returned(self, db):
        """Prospector handles multiple Exa results correctly."""
        companies = [
            {"name": "Summit 3PL", "domain": "summit3pl.com", "industry": "Logistics",
             "annual_revenue": 600_000_000, "facility_count": 12, "hq_country": "US",
             "wms_detected": True, "automation_footprint": False},
            {"name": "Apex Food Group", "domain": "apexfood.com", "industry": "Food_Bev",
             "annual_revenue": 900_000_000, "facility_count": 20, "hq_country": "US",
             "wms_detected": False, "automation_footprint": True},
        ]
        mock_exa = MagicMock()
        mock_exa.search.return_value = [
            {"title": c["name"], "url": f"https://{c['domain']}", "text": "..."} for c in companies
        ]
        mock_clay = MagicMock()
        mock_clay.get_company.side_effect = companies

        agent = ProspectorAgent(db=db, exa_client=mock_exa, clay_client=mock_clay)
        results = agent.run()

        assert len(results) == 2
        assert db.query(Account).count() == 2


# ---------------------------------------------------------------------------
# ICPQualifierAgent tests
# ---------------------------------------------------------------------------

class TestICPQualifierAgent:

    def test_high_fit_company_scores_above_40(self, db):
        """A company meeting most ICP criteria scores ≥ 40."""
        account = Account(
            company_name="Summit 3PL", domain="summit3pl.com",
            industry="Logistics", annual_revenue=800_000_000,
            facility_count=15, hq_country="US",
            wms_detected=True, automation_footprint=False,
            status=AccountStatus.researching
        )
        db.add(account)
        db.commit()

        agent = ICPQualifierAgent(db=db)
        result = agent.score(account)

        assert result["icp_score"] >= 40
        assert result["pass"] is True

    def test_low_fit_company_scores_below_40(self, db):
        """A company missing key ICP criteria scores < 40 and is disqualified."""
        account = Account(
            company_name="Corner Store LLC", domain="cornerstore.com",
            industry="Retail", annual_revenue=520_000_000,
            facility_count=3, hq_country="US",
            wms_detected=False, automation_footprint=False,
            status=AccountStatus.researching
        )
        db.add(account)
        db.commit()

        agent = ICPQualifierAgent(db=db)
        result = agent.score(account)

        assert result["icp_score"] < 40
        assert result["pass"] is False

    def test_disqualified_account_status_updated(self, db):
        """Account status is set to 'disqualified' when score < 40."""
        account = Account(
            company_name="Corner Store LLC", domain="cornerstore.com",
            industry="Retail", annual_revenue=520_000_000,
            facility_count=3, hq_country="US",
            wms_detected=False, automation_footprint=False,
        )
        db.add(account)
        db.commit()

        agent = ICPQualifierAgent(db=db)
        agent.score(account)
        db.refresh(account)

        assert account.status == AccountStatus.disqualified
        assert account.disqualification_reason is not None

    def test_qualified_account_status_updated(self, db):
        """Account status is set to 'qualified' when score ≥ 40."""
        account = Account(
            company_name="Summit 3PL", domain="summit3pl.com",
            industry="Logistics", annual_revenue=800_000_000,
            facility_count=15, hq_country="US",
            wms_detected=True, automation_footprint=False,
        )
        db.add(account)
        db.commit()

        agent = ICPQualifierAgent(db=db)
        agent.score(account)
        db.refresh(account)

        assert account.status == AccountStatus.qualified

    def test_score_components_are_correct(self, db):
        """ICP score components add up correctly for a known input."""
        account = Account(
            company_name="Perfect ICP Co", domain="perfecticp.com",
            industry="Logistics",
            annual_revenue=1_500_000_000,   # 1B+ = 25 pts
            facility_count=30,              # 25+ = 25 pts
            hq_country="US",
            wms_detected=True,             # 15 pts
            automation_footprint=True,     # 15 pts
            # vertical exact match         # 20 pts → total = 100
        )
        db.add(account)
        db.commit()

        agent = ICPQualifierAgent(db=db)
        result = agent.score(account)

        assert result["icp_score"] == 100

    def test_revenue_between_500m_and_1b_scores_15_pts(self, db):
        """Revenue between $500M-$1B contributes 15 revenue points."""
        account = Account(
            company_name="Mid Range Co", domain="midrange.com",
            industry="Logistics", annual_revenue=700_000_000,
            facility_count=30, hq_country="US",
            wms_detected=True, automation_footprint=True,
        )
        db.add(account)
        db.commit()

        agent = ICPQualifierAgent(db=db)
        result = agent.score(account)

        assert result["score_breakdown"]["revenue"] == 15

    def test_revenue_above_1b_scores_25_pts(self, db):
        """Revenue above $1B contributes 25 revenue points."""
        account = Account(
            company_name="Big Co", domain="bigco.com",
            industry="Logistics", annual_revenue=2_000_000_000,
            facility_count=30, hq_country="US",
            wms_detected=True, automation_footprint=True,
        )
        db.add(account)
        db.commit()

        agent = ICPQualifierAgent(db=db)
        result = agent.score(account)

        assert result["score_breakdown"]["revenue"] == 25

    def test_non_icp_vertical_scores_zero(self, db):
        """A non-ICP vertical (e.g. Financial Services) scores 0 for vertical."""
        account = Account(
            company_name="Bank Corp", domain="bankcorp.com",
            industry="Financial_Services", annual_revenue=1_000_000_000,
            facility_count=20, hq_country="US",
            wms_detected=False, automation_footprint=False,
        )
        db.add(account)
        db.commit()

        agent = ICPQualifierAgent(db=db)
        result = agent.score(account)

        assert result["score_breakdown"]["vertical"] == 0

    def test_icp_score_saved_to_database(self, db):
        """ICP score is persisted on the Account record after scoring."""
        account = Account(
            company_name="Summit 3PL", domain="summit3pl.com",
            industry="Logistics", annual_revenue=800_000_000,
            facility_count=15, hq_country="US",
            wms_detected=True, automation_footprint=False,
        )
        db.add(account)
        db.commit()

        agent = ICPQualifierAgent(db=db)
        agent.score(account)
        db.refresh(account)

        assert account.icp_score > 0
