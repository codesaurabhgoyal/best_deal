from __future__ import annotations
from src.discovery.base import DiscoveryProvider

DEMO_INDEX = {
    "rolex 116610ln": [
        "https://demo-watch-a.example/listing/1",
        "https://demo-watch-b.example/item/alpha",
    ],
    "omega 311.30.42.30.01.005": [
        "https://demo-watch-a.example/listing/2",
        "https://demo-watch-b.example/item/gamma",
    ],
    "ray-ban rb2140 901 50-22": [
        "https://demo-sunglass-a.example/p/1",
        "https://demo-sunglass-b.example/item/x",
    ],
}

class DemoDiscovery(DiscoveryProvider):
    code = "demo"
    def discover_urls(self, query: str, max_results: int = 10) -> list[str]:
        q = (query or "").strip().lower()
        return (DEMO_INDEX.get(q, [])[:max_results])
