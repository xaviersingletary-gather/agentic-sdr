import httpx
from src.config import HUBSPOT_ACCESS_TOKEN

BASE_URL = "https://api.hubapi.com"


class HubSpotClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

    def get_contact(self, email: str) -> dict | None:
        """Look up a contact by email. Returns None if not found."""
        resp = httpx.get(
            f"{BASE_URL}/crm/v3/objects/contacts/search",
            headers=self.headers,
            json={"filterGroups": [{"filters": [{"propertyName": "email", "operator": "EQ", "value": email}]}]},
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        return results[0] if results else None

    def log_activity(self, contact_id: str, note: str) -> dict:
        """Log an outreach activity note on a HubSpot contact."""
        resp = httpx.post(
            f"{BASE_URL}/crm/v3/objects/notes",
            headers=self.headers,
            json={"properties": {"hs_note_body": note, "hs_timestamp": "now"}},
        )
        resp.raise_for_status()
        return resp.json()

    def create_task(self, contact_id: str, subject: str, body: str, owner_id: str) -> dict:
        """Create a follow-up task assigned to Rob when a positive reply is detected."""
        resp = httpx.post(
            f"{BASE_URL}/crm/v3/objects/tasks",
            headers=self.headers,
            json={"properties": {"hs_task_subject": subject, "hs_task_body": body, "hs_task_status": "NOT_STARTED"}},
        )
        resp.raise_for_status()
        return resp.json()

    def update_contact_status(self, contact_id: str, status: str) -> dict:
        """Update a contact's lifecycle stage or custom status property."""
        resp = httpx.patch(
            f"{BASE_URL}/crm/v3/objects/contacts/{contact_id}",
            headers=self.headers,
            json={"properties": {"sdr_status": status}},
        )
        resp.raise_for_status()
        return resp.json()
