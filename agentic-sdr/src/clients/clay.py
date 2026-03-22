import httpx
from src.config import CLAY_API_KEY

BASE_URL = "https://api.clay.com/v1"


class ClayClient:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {CLAY_API_KEY}", "Content-Type": "application/json"}

    def search_companies(self, filters: dict) -> list[dict]:
        """Search for companies by ICP filters. Returns list of company records."""
        raise NotImplementedError("Clay company search — wire in Phase 2")

    def get_company(self, domain: str) -> dict:
        """Enrich a company by domain. Returns firmographic + technographic data."""
        raise NotImplementedError("Clay company enrichment — wire in Phase 2")

    def get_job_postings(self, company_name: str) -> list[dict]:
        """Fetch recent job postings for a company. Returns list of job records."""
        raise NotImplementedError("Clay job postings — wire in Phase 3")
