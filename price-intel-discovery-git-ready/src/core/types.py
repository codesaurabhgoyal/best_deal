from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class OfferIn(BaseModel):
    site_code: str
    product_type: str
    url: str
    title_raw: str
    brand: Optional[str] = None
    model: Optional[str] = None
    identifiers: Dict[str, Any] = {}

    currency: str = "EUR"
    base_price: float
    shipping_cost: float = 0.0
    tax_estimate: float = 0.0
    payment_fee: float = 0.0
    coupon_value: float = 0.0
    cashback_value: float = 0.0

    availability: str = "in_stock"
    seller_rating: Optional[float] = None
    delivery_days: Optional[int] = None
    captured_at: datetime = datetime.utcnow()

class BestDealOut(BaseModel):
    product_type: str
    identity_key: str
    winner_offer_id: int
    winner_site: str
    winner_total_price: float
    runner_up_total_price: float | None
    savings_vs_runner_up: float | None
