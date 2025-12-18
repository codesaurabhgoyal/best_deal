from __future__ import annotations
import re
from src.product_types.base import ProductTypeStrategy
from src.core.types import OfferIn

ROLEX = re.compile(r"\b(\d{6}[A-Z]{0,3})\b")
OMEGA = re.compile(r"\b(\d{3}\.\d{2}\.\d{2}\.\d{2}\.\d{2}\.\d{3})\b")

class WatchStrategy(ProductTypeStrategy):
    code = "watch"
    def make_identity_key(self, offer: OfferIn) -> str:
        ref = offer.identifiers.get("reference")
        if not ref:
            m = ROLEX.search(offer.title_raw) or OMEGA.search(offer.title_raw)
            if m:
                ref = m.group(1)
        if not ref:
            raise ValueError("Watch offer missing 'reference'.")
        return str(ref).strip()
