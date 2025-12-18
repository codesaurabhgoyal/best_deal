from __future__ import annotations
from abc import ABC, abstractmethod
from src.core.types import OfferIn

class ProductTypeStrategy(ABC):
    code: str
    @abstractmethod
    def make_identity_key(self, offer: OfferIn) -> str:
        raise NotImplementedError
