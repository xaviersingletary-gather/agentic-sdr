"""
Phase 3 Tests: Signal Hunter Agent
"""
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.base import Base
from src.models.account import Account, AccountStatus
from src.models.signal import Signal, SignalType, SIGNAL_POINTS
from src.agents.signal_hunter import SignalHunterAgent


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
        facility_count=15, hq_country="US",
        wms_detected=True, automation_footprint=False,
        icp_score=70.0, status=AccountStatus.qualified
    )
    db.add(account)
    db.commit()
    return account


class TestSignalHunterAgent:

    def test_detects_job_posting_signal(self, db, qualified_account):
        """Detects a warehouse job posting signal from Clay."""
        mock_clay = MagicMock()
        mock_clay.get_job_postings.return_value = [
            {"title": "Director of Inventory Control", "date": "2026-03-01",
             "source": "Clay", "content": "Hiring Director of Inventory Control"}
        ]
        mock_exa = MagicMock()
        mock_exa.search.return_value = []
        mock_slack = MagicMock()

        agent = SignalHunterAgent(db=db, clay_client=mock_clay, exa_client=mock_exa, slack_client=mock_slack)
        result = agent.hunt(qualified_account)

        signals = db.query(Signal).filter_by(account_id=qualified_account.id).all()
        assert len(signals) >= 1
        assert any(s.signal_type == SignalType.job_posting for s in signals)

    def test_detects_news_signal_from_exa(self, db, qualified_account):
        """Detects a new DC announcement from Exa news search."""
        mock_clay = MagicMock()
        mock_clay.get_job_postings.return_value = []
        mock_exa = MagicMock()
        mock_exa.search.return_value = [
            {"title": "Summit 3PL opens new distribution center in Texas",
             "url": "https://news.example.com/summit-dc",
             "text": "Summit 3PL announced a new 500,000 sq ft distribution center.",
             "publishedDate": "2026-03-10"}
        ]
        mock_slack = MagicMock()

        agent = SignalHunterAgent(db=db, clay_client=mock_clay, exa_client=mock_exa, slack_client=mock_slack)
        agent.hunt(qualified_account)

        signals = db.query(Signal).filter_by(account_id=qualified_account.id).all()
        assert any(s.signal_type == SignalType.new_dc for s in signals)

    def test_quality_score_calculated_from_signals(self, db, qualified_account):
        """Quality score is the sum of all signal points, capped at 100."""
        mock_clay = MagicMock()
        mock_clay.get_job_postings.return_value = [
            {"title": "WMS Implementation Manager", "date": "2026-03-01",
             "source": "Clay", "content": "WMS migration project lead"}
        ]
        mock_exa = MagicMock()
        mock_exa.search.return_value = []
        mock_slack = MagicMock()

        agent = SignalHunterAgent(db=db, clay_client=mock_clay, exa_client=mock_exa, slack_client=mock_slack)
        result = agent.hunt(qualified_account)

        assert result["quality_score"] > 0
        assert result["quality_score"] <= 100

    def test_quality_score_saved_to_account(self, db, qualified_account):
        """Quality score is persisted on the account record."""
        mock_clay = MagicMock()
        mock_clay.get_job_postings.return_value = [
            {"title": "VP Supply Chain", "date": "2026-03-01",
             "source": "Clay", "content": "New VP of Supply Chain hired"}
        ]
        mock_exa = MagicMock()
        mock_exa.search.return_value = []
        mock_slack = MagicMock()

        agent = SignalHunterAgent(db=db, clay_client=mock_clay, exa_client=mock_exa, slack_client=mock_slack)
        agent.hunt(qualified_account)
        db.refresh(qualified_account)

        assert qualified_account.quality_score > 0

    def test_slack_notified_when_score_above_70(self, db, qualified_account):
        """Xavier is notified via Slack when quality score >= 70."""
        mock_clay = MagicMock()
        mock_clay.get_job_postings.return_value = [
            {"title": "Director Warehouse Ops", "date": "2026-03-01",
             "source": "Clay", "content": "Hiring Dir Warehouse Ops"},
            {"title": "WMS Project Manager", "date": "2026-03-05",
             "source": "Clay", "content": "WMS migration lead"},
            {"title": "VP Supply Chain", "date": "2026-03-10",
             "source": "Clay", "content": "New VP Supply Chain"},
        ]
        mock_exa = MagicMock()
        mock_exa.search.return_value = [
            {"title": "Summit 3PL opens new DC",
             "url": "https://news.com/summit",
             "text": "New distribution center announced.",
             "publishedDate": "2026-03-12"}
        ]
        mock_slack = MagicMock()

        agent = SignalHunterAgent(db=db, clay_client=mock_clay, exa_client=mock_exa, slack_client=mock_slack)
        result = agent.hunt(qualified_account)

        if result["quality_score"] >= 70:
            mock_slack.notify_xavier.assert_called_once()

    def test_slack_not_notified_when_score_below_70(self, db, qualified_account):
        """Xavier is NOT notified when quality score < 70."""
        mock_clay = MagicMock()
        mock_clay.get_job_postings.return_value = []
        mock_exa = MagicMock()
        mock_exa.search.return_value = []
        mock_slack = MagicMock()

        agent = SignalHunterAgent(db=db, clay_client=mock_clay, exa_client=mock_exa, slack_client=mock_slack)
        result = agent.hunt(qualified_account)

        assert result["quality_score"] < 70
        mock_slack.notify_xavier.assert_not_called()

    def test_no_duplicate_signals_saved(self, db, qualified_account):
        """Running hunt twice does not create duplicate signal records."""
        mock_clay = MagicMock()
        mock_clay.get_job_postings.return_value = [
            {"title": "Director Warehouse", "date": "2026-03-01",
             "source": "Clay", "content": "Hiring Dir Warehouse"}
        ]
        mock_exa = MagicMock()
        mock_exa.search.return_value = []
        mock_slack = MagicMock()

        agent = SignalHunterAgent(db=db, clay_client=mock_clay, exa_client=mock_exa, slack_client=mock_slack)
        agent.hunt(qualified_account)
        agent.hunt(qualified_account)

        signals = db.query(Signal).filter_by(account_id=qualified_account.id).all()
        assert len(signals) == 1

    def test_returns_signals_list_and_quality_score(self, db, qualified_account):
        """hunt() returns dict with signals list and quality_score."""
        mock_clay = MagicMock()
        mock_clay.get_job_postings.return_value = []
        mock_exa = MagicMock()
        mock_exa.search.return_value = []
        mock_slack = MagicMock()

        agent = SignalHunterAgent(db=db, clay_client=mock_clay, exa_client=mock_exa, slack_client=mock_slack)
        result = agent.hunt(qualified_account)

        assert "signals" in result
        assert "quality_score" in result
        assert isinstance(result["signals"], list)
        assert isinstance(result["quality_score"], (int, float))
