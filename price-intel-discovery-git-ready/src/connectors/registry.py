from __future__ import annotations
from typing import List
from src.connectors.base import Connector
from src.connectors.demo_watch_a import DemoWatchA
from src.connectors.demo_watch_b import DemoWatchB
from src.connectors.demo_sunglass_a import DemoSunglassA
from src.connectors.demo_sunglass_b import DemoSunglassB

_CONNECTORS: List[Connector] = [DemoWatchA(), DemoWatchB(), DemoSunglassA(), DemoSunglassB()]

def list_connectors() -> list[dict]:
    return [{"code": c.code, "name": c.name} for c in _CONNECTORS]

def route_urls(urls: list[str]) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {}
    for u in urls:
        for c in _CONNECTORS:
            if c.supports(u):
                buckets.setdefault(c.code, []).append(u)
                break
    return buckets

def get_connector_by_code(code: str) -> Connector:
    for c in _CONNECTORS:
        if c.code == code:
            return c
    raise KeyError(f"Unknown connector code: {code}")
