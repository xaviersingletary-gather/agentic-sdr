from src.models.account import Account, AccountStatus
from src.exclusions.checker import check_exclusion

REVENUE_FLOOR = 500_000_000

ICP_SEARCH_QUERIES = [
    "third party logistics 3PL warehouse distribution center operations",
    "food and beverage distribution warehouse management",
    "pharmaceutical cold chain warehouse distribution",
    "retail distribution center warehouse fulfillment",
    "manufacturing distribution warehouse operations",
    "CPG consumer packaged goods warehouse distribution network",
]


class ProspectorAgent:
    def __init__(self, db, exa_client, clay_client):
        self.db = db
        self.exa = exa_client
        self.clay = clay_client

    def run(self) -> list[Account]:
        saved = []
        seen_domains = set()

        for query in ICP_SEARCH_QUERIES:
            results = self.exa.search(query)
            for result in results:
                domain = self._extract_domain(result.get("url", ""))
                if not domain or domain in seen_domains:
                    continue

                company_data = self.clay.get_company(domain)
                if not company_data:
                    continue

                company_name = company_data.get("name", "")
                revenue = company_data.get("annual_revenue") or 0

                # Hard revenue floor
                if revenue < REVENUE_FLOOR:
                    continue

                # Exclusion check
                exclusion = check_exclusion(company_name)
                if exclusion["excluded"]:
                    continue

                # Deduplication — skip if domain already in DB
                existing = self.db.query(Account).filter_by(domain=domain).first()
                if existing:
                    seen_domains.add(domain)
                    continue

                account = Account(
                    company_name=company_name,
                    domain=domain,
                    industry=company_data.get("industry"),
                    annual_revenue=revenue,
                    facility_count=company_data.get("facility_count"),
                    hq_country=company_data.get("hq_country"),
                    wms_detected=company_data.get("wms_detected", False),
                    automation_footprint=company_data.get("automation_footprint", False),
                    status=AccountStatus.researching,
                )
                self.db.add(account)
                self.db.commit()
                saved.append(account)
                seen_domains.add(domain)

        return saved

    @staticmethod
    def _extract_domain(url: str) -> str | None:
        if not url:
            return None
        url = url.replace("https://", "").replace("http://", "").split("/")[0]
        return url.lower() if url else None
