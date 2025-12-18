from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import desc
from src.db.models import Product, Offer, Site
from src.core.score import deal_score
from src.core.types import BestDealOut

def best_deal(db: Session, product_type: str, identity_key: str) -> BestDealOut | None:
    prod = (db.query(Product)
            .filter(Product.product_type == product_type)
            .filter(Product.identity_key == identity_key)
            .one_or_none())
    if not prod:
        return None

    rows = (db.query(Offer, Site)
            .join(Site, Offer.site_id == Site.id)
            .filter(Offer.product_id == prod.id)
            .filter(Offer.availability == "in_stock")
            .order_by(desc(Offer.captured_at))
            .all())
    if not rows:
        return None

    scored = []
    for offer, site in rows:
        s = deal_score(float(offer.total_price), offer.delivery_days,
                       float(offer.seller_rating) if offer.seller_rating is not None else None)
        scored.append((s, offer, site))
    scored.sort(key=lambda x: x[0])
    winner = scored[0]
    runner = scored[1] if len(scored) > 1 else None

    return BestDealOut(
        product_type=product_type,
        identity_key=identity_key,
        winner_offer_id=winner[1].id,
        winner_site=winner[2].code,
        winner_total_price=float(winner[1].total_price),
        runner_up_total_price=float(runner[1].total_price) if runner else None,
        savings_vs_runner_up=(float(runner[1].total_price) - float(winner[1].total_price)) if runner else None,
    )
