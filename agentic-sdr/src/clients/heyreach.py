import httpx
from src.config import HEYREACH_API_KEY

BASE_URL = "https://api.heyreach.io/api/public"


class HeyReachClient:
    def __init__(self):
        self.headers = {"X-API-KEY": HEYREACH_API_KEY, "Content-Type": "application/json"}

    def add_to_campaign(self, campaign_id: str, linkedin_url: str, personalization: dict) -> dict:
        """Add a contact to a HeyReach LinkedIn campaign."""
        raise NotImplementedError("HeyReach campaign enrollment — wire in Phase 5")

    def get_campaign_activity(self, campaign_id: str) -> list[dict]:
        """Fetch replies and connection status from a campaign."""
        raise NotImplementedError("HeyReach activity polling — wire in Phase 6")
