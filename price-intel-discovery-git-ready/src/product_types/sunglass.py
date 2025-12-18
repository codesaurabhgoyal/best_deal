from __future__ import annotations
from src.product_types.base import ProductTypeStrategy
from src.core.types import OfferIn

class SunglassStrategy(ProductTypeStrategy):
    code = "sunglass"
    def make_identity_key(self, offer: OfferIn) -> str:
        gtin = offer.identifiers.get("gtin") or offer.identifiers.get("ean") or offer.identifiers.get("upc")
        if gtin:
            return str(gtin).strip()
        brand = (offer.brand or offer.identifiers.get("brand") or "").strip().lower()
        model_code = (offer.identifiers.get("model_code") or "").strip().lower()
        color = (offer.identifiers.get("color") or "").strip().lower()
        size = (offer.identifiers.get("size") or "").strip().lower()
        if not (brand and model_code):
            raise ValueError("Sunglass offer missing GTIN and brand+model_code fallback.")
        return "|".join([brand, model_code, color, size]).strip("|")
