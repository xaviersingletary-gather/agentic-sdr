import httpx
from src.config import EXA_API_KEY

BASE_URL = "https://api.exa.ai"


class ExaClient:
    def __init__(self):
        self.headers = {"x-api-key": EXA_API_KEY, "Content-Type": "application/json"}

    def search(self, query: str, num_results: int = 10) -> list[dict]:
        """Web search for ICP-fit companies or buying signals."""
        raise NotImplementedError("Exa search — wire in Phase 2")

    def find_similar(self, url: str, num_results: int = 10) -> list[dict]:
        """Find companies similar to a known ICP-fit company."""
        raise NotImplementedError("Exa find_similar — wire in Phase 2")
