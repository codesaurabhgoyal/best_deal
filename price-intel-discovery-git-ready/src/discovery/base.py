from __future__ import annotations
from abc import ABC, abstractmethod

class DiscoveryProvider(ABC):
    code: str
    @abstractmethod
    def discover_urls(self, query: str, max_results: int = 10) -> list[str]:
        raise NotImplementedError
