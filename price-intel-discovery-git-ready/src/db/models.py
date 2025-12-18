from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Numeric, ForeignKey, UniqueConstraint, Index
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Site(Base):
    __tablename__ = "sites"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    offers = relationship("Offer", back_populates="site")

class Product(Base):
    __tablename__ = "products"
    __table_args__ = (UniqueConstraint("product_type", "identity_key", name="uq_product_type_identity"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_type: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    identity_key: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    brand: Mapped[str | None] = mapped_column(String(80), index=True, nullable=True)
    model: Mapped[str | None] = mapped_column(String(200), index=True, nullable=True)
    title_norm: Mapped[str | None] = mapped_column(String(400), index=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    offers = relationship("Offer", back_populates="product")

class Offer(Base):
    __tablename__ = "offers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    title_raw: Mapped[str] = mapped_column(String(500), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False)
    base_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    shipping_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    tax_estimate: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    payment_fee: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    coupon_value: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    cashback_value: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    total_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, index=True)
    availability: Mapped[str] = mapped_column(String(40), nullable=False, default="in_stock")
    seller_rating: Mapped[float | None] = mapped_column(Numeric(4, 2), nullable=True)
    delivery_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    site = relationship("Site", back_populates="offers")
    product = relationship("Product", back_populates="offers")

Index("ix_offers_site_product_time", Offer.site_id, Offer.product_id, Offer.captured_at)
