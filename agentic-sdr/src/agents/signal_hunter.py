from src.models.account import Account
from src.models.signal import Signal, SignalType, SignalSource, SIGNAL_POINTS
from src.config import QUALITY_SCORE_NOTIFY_THRESHOLD

WAREHOUSE_JOB_KEYWORDS = [
    "warehouse", "distribution", "inventory", "supply chain", "wms",
    "fulfillment", "logistics", "continuous improvement", "3pl", "dc operations"
]

WMS_KEYWORDS = ["wms", "warehouse management system", "wms implementation", "wms migration"]
NEW_DC_KEYWORDS = ["new distribution center", "new warehouse", "new dc", "new facility",
                   "opens distribution", "expands distribution", "new fulfillment center"]
AUTOMATION_KEYWORDS = ["automation", "autonomous", "robots", "amr", "automated guided"]
AUDIT_KEYWORDS = ["osha", "audit", "citation", "violation", "recall", "safety incident"]


def _classify_job_signal(content: str) -> SignalType:
    content_lower = content.lower()
    if any(k in content_lower for k in WMS_KEYWORDS):
        return SignalType.wms_migration
    if any(k in content_lower for k in WAREHOUSE_JOB_KEYWORDS):
        return SignalType.job_posting
    return SignalType.job_posting


def _classify_news_signal(content: str) -> SignalType | None:
    content_lower = content.lower()
    if any(k in content_lower for k in NEW_DC_KEYWORDS):
        return SignalType.new_dc
    if any(k in content_lower for k in WMS_KEYWORDS):
        return SignalType.wms_migration
    if any(k in content_lower for k in AUTOMATION_KEYWORDS):
        return SignalType.automation_adoption
    if any(k in content_lower for k in AUDIT_KEYWORDS):
        return SignalType.audit_failure
    return None


class SignalHunterAgent:
    def __init__(self, db, clay_client, exa_client, slack_client):
        self.db = db
        self.clay = clay_client
        self.exa = exa_client
        self.slack = slack_client

    def hunt(self, account: Account) -> dict:
        new_signals = []

        # --- Clay: job postings ---
        job_postings = self.clay.get_job_postings(account.company_name)
        for job in job_postings:
            content = job.get("content", "") or job.get("title", "")
            signal_type = _classify_job_signal(content)
            if not self._already_saved(account.id, signal_type, SignalSource.clay):
                signal = Signal(
                    account_id=account.id,
                    signal_type=signal_type,
                    signal_source=SignalSource.clay,
                    raw_content=content,
                    points_contributed=float(SIGNAL_POINTS.get(signal_type, 0)),
                )
                self.db.add(signal)
                new_signals.append(signal)

        # --- Exa: news signals ---
        news_results = self.exa.search(f"{account.company_name} warehouse distribution supply chain")
        for article in news_results:
            # Combine title + text so keywords spanning both fields are caught
            content = " ".join(filter(None, [article.get("title", ""), article.get("text", "")]))
            signal_type = _classify_news_signal(content)
            if signal_type and not self._already_saved(account.id, signal_type, SignalSource.exa):
                signal = Signal(
                    account_id=account.id,
                    signal_type=signal_type,
                    signal_source=SignalSource.exa,
                    raw_content=content,
                    points_contributed=float(SIGNAL_POINTS.get(signal_type, 0)),
                )
                self.db.add(signal)
                new_signals.append(signal)

        self.db.commit()

        # Recalculate total quality score from all signals on this account
        all_signals = self.db.query(Signal).filter_by(account_id=account.id).all()
        quality_score = min(100.0, sum(s.points_contributed for s in all_signals))

        account.quality_score = quality_score
        self.db.commit()

        # Notify Xavier if score >= threshold
        if quality_score >= QUALITY_SCORE_NOTIFY_THRESHOLD:
            self.slack.notify_xavier(
                company_name=account.company_name,
                quality_score=quality_score,
                signals=[{"signal_type": s.signal_type,
                          "points_contributed": s.points_contributed,
                          "signal_source": s.signal_source} for s in all_signals],
            )

        return {
            "signals": [{"signal_type": s.signal_type,
                          "points_contributed": s.points_contributed,
                          "signal_source": s.signal_source} for s in all_signals],
            "quality_score": quality_score,
        }

    def _already_saved(self, account_id: int, signal_type: str, signal_source: str) -> bool:
        return self.db.query(Signal).filter_by(
            account_id=account_id,
            signal_type=signal_type,
            signal_source=signal_source,
        ).first() is not None
