from __future__ import annotations
from src.settings import settings
from src.discovery.demo import DemoDiscovery
from src.discovery.bing import BingDiscovery
from src.discovery.google_cse import GoogleCSEDiscovery

def get_provider():
    code = settings.discovery_provider
    if code == "demo":
        return DemoDiscovery()
    if code == "bing":
        return BingDiscovery()
    if code == "google_cse":
        return GoogleCSEDiscovery()
    raise KeyError(f"Unknown DISCOVERY_PROVIDER='{code}'. Use demo|bing|google_cse.")
