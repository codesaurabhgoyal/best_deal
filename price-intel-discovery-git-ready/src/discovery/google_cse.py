from __future__ import annotations
import httpx
from src.discovery.base import DiscoveryProvider
from src.settings import settings

class GoogleCSEDiscovery(DiscoveryProvider):
    code = "google_cse"
    def discover_urls(self, query: str, max_results: int = 10) -> list[str]:
        if not settings.google_cse_api_key or not settings.google_cse_cx:
            raise ValueError("GOOGLE_CSE_API_KEY / GOOGLE_CSE_CX not set.")
        params = {"key": settings.google_cse_api_key, "cx": settings.google_cse_cx, "q": query, "num": min(max_results, 10)}
        r = httpx.get("https://www.googleapis.com/customsearch/v1", params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        items = data.get("items") or []
        return [it["link"] for it in items if "link" in it]
