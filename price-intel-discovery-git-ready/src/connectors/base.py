from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence
from src.core.types import OfferIn

class Connector(ABC):
    code: str
    name: str

    @abstractmethod
    def supports(self, url: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def fetch_offers(self, urls: Sequence[str]) -> list[OfferIn]:
        raise NotImplementedError
