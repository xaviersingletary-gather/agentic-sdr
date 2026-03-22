from src.models.account import Account, AccountStatus

ICP_VERTICALS = ["Logistics", "Food_Bev", "Healthcare_Pharma", "Retail", "Manufacturing", "CPG"]


class ICPQualifierAgent:
    PASS_THRESHOLD = 40

    def __init__(self, db):
        self.db = db

    def score(self, account: Account) -> dict:
        breakdown = {
            "revenue": self._score_revenue(account.annual_revenue),
            "facilities": self._score_facilities(account.facility_count),
            "vertical": self._score_vertical(account.industry),
            "wms": 15 if account.wms_detected else 0,
            "automation": 15 if account.automation_footprint else 0,
        }
        total = sum(breakdown.values())
        passed = total >= self.PASS_THRESHOLD

        account.icp_score = float(total)
        if passed:
            account.status = AccountStatus.qualified
            account.disqualification_reason = None
        else:
            account.status = AccountStatus.disqualified
            account.disqualification_reason = (
                f"ICP score {total}/100 below threshold {self.PASS_THRESHOLD}. "
                f"Breakdown: {breakdown}"
            )
        self.db.commit()

        return {
            "icp_score": float(total),
            "pass": passed,
            "score_breakdown": breakdown,
            "disqualification_reason": account.disqualification_reason,
        }

    @staticmethod
    def _score_revenue(revenue: float | None) -> int:
        if not revenue:
            return 0
        if revenue >= 1_000_000_000:
            return 25
        if revenue >= 500_000_000:
            return 15
        return 0

    @staticmethod
    def _score_facilities(count: int | None) -> int:
        if not count:
            return 0
        if count >= 25:
            return 25
        if count >= 11:
            return 15
        return 0

    @staticmethod
    def _score_vertical(industry: str | None) -> int:
        if not industry:
            return 0
        return 20 if industry in ICP_VERTICALS else 0
