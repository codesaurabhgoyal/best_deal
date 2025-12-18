"""init schema

Revision ID: 0001_init
Revises:
Create Date: 2025-12-18
"""
from __future__ import annotations
from alembic import op
import sqlalchemy as sa

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "sites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=50), nullable=False, unique=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_type", sa.String(length=40), nullable=False, index=True),
        sa.Column("identity_key", sa.String(length=200), nullable=False, index=True),
        sa.Column("brand", sa.String(length=80), nullable=True, index=True),
        sa.Column("model", sa.String(length=200), nullable=True, index=True),
        sa.Column("title_norm", sa.String(length=400), nullable=True, index=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("product_type", "identity_key", name="uq_product_type_identity"),
    )

    op.create_table(
        "offers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("sites.id"), nullable=False, index=True),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False, index=True),
        sa.Column("url", sa.String(length=1000), nullable=False),
        sa.Column("title_raw", sa.String(length=500), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("base_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("shipping_cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("tax_estimate", sa.Numeric(12, 2), nullable=False),
        sa.Column("payment_fee", sa.Numeric(12, 2), nullable=False),
        sa.Column("coupon_value", sa.Numeric(12, 2), nullable=False),
        sa.Column("cashback_value", sa.Numeric(12, 2), nullable=False),
        sa.Column("total_price", sa.Numeric(12, 2), nullable=False, index=True),
        sa.Column("availability", sa.String(length=40), nullable=False),
        sa.Column("seller_rating", sa.Numeric(4, 2), nullable=True),
        sa.Column("delivery_days", sa.Integer(), nullable=True),
        sa.Column("captured_at", sa.DateTime(), nullable=False, index=True),
    )

def downgrade() -> None:
    op.drop_table("offers")
    op.drop_table("products")
    op.drop_table("sites")
