from __future__ import annotations
from src.settings import settings

def deal_score(total_price: float, delivery_days: int | None, seller_rating: float | None) -> float:
    delivery_penalty = (delivery_days or 0) * settings.weight_delivery_days
    rating_bonus = (seller_rating or 0) * settings.weight_seller_rating
    return (total_price * settings.weight_price) + delivery_penalty - rating_bonus
