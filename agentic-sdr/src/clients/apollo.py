import httpx
from src.config import APOLLO_API_KEY

BASE_URL = "https://api.apollo.io/v1"


class ApolloClient:
    def __init__(self):
        self.headers = {"x-api-key": APOLLO_API_KEY, "Content-Type": "application/json"}

    def search_people(self, company_name: str, titles: list[str]) -> list[dict]:
        """Search for contacts at a company by title keywords."""
        raise NotImplementedError("Apollo people search — wire in Phase 4")

    def enrich_contact(self, linkedin_url: str) -> dict:
        """Enrich a contact record with verified email and phone."""
        raise NotImplementedError("Apollo contact enrichment — wire in Phase 4")

    def create_sequence(self, contact_id: str, sequence_id: str) -> dict:
        """Enroll a contact in an Apollo email sequence."""
        raise NotImplementedError("Apollo sequence enrollment — wire in Phase 5")
