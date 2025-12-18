from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Session
from src.db.models import Site, Product, Offer
from src.core.types import OfferIn
from src.core.normalize import normalize_title, compute_total
from src.product_types.registry import get_strategy

def upsert_site(db: Session, site_code: str, site_name: str) -> Site:
    site = db.query(Site).filter(Site.code == site_code).one_or_none()
    if site:
        return site
    site = Site(code=site_code, name=site_name, created_at=datetime.utcnow())
    db.add(site); db.flush()
    return site

def find_or_create_product(db: Session, offer: OfferIn) -> Product:
    strategy = get_strategy(offer.product_type)
    identity_key = strategy.make_identity_key(offer)
    prod = (db.query(Product)
            .filter(Product.product_type == offer.product_type)
            .filter(Product.identity_key == identity_key)
            .one_or_none())
    if prod:
        return prod
    prod = Product(
        product_type=offer.product_type,
        identity_key=identity_key,
        brand=offer.brand,
        model=offer.model,
        title_norm=normalize_title(offer.title_raw),
        created_at=datetime.utcnow(),
    )
    db.add(prod); db.flush()
    return prod

def insert_offer(db: Session, site: Site, product: Product, offer: OfferIn) -> Offer:
    total = compute_total(offer.base_price, offer.shipping_cost, offer.tax_estimate,
                          offer.payment_fee, offer.coupon_value, offer.cashback_value)
    obj = Offer(
        site_id=site.id, product_id=product.id, url=offer.url, title_raw=offer.title_raw,
        currency=offer.currency, base_price=offer.base_price, shipping_cost=offer.shipping_cost,
        tax_estimate=offer.tax_estimate, payment_fee=offer.payment_fee, coupon_value=offer.coupon_value,
        cashback_value=offer.cashback_value, total_price=total, availability=offer.availability,
        seller_rating=offer.seller_rating, delivery_days=offer.delivery_days, captured_at=offer.captured_at
    )
    db.add(obj)
    return obj
