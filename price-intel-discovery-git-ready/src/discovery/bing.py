from __future__ import annotations
import httpx
from src.discovery.base import DiscoveryProvider
from src.settings import settings

class BingDiscovery(DiscoveryProvider):
    code = "bing"
    def discover_urls(self, query: str, max_results: int = 10) -> list[str]:
        if not settings.bing_api_key:
            raise ValueError("BING_API_KEY is not set.")
        headers = {"Ocp-Apim-Subscription-Key": settings.bing_api_key}
        params = {"q": query, "count": max_results, "responseFilter": "Webpages"}
        r = httpx.get(settings.bing_endpoint, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        items = (data.get("webPages") or {}).get("value") or []
        return [it["url"] for it in items if "url" in it]
