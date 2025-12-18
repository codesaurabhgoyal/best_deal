from __future__ import annotations
from pathlib import Path
from urllib.parse import urlparse
from selectolax.parser import HTMLParser
from src.connectors.base import Connector
from src.core.types import OfferIn

FIXTURE = Path(__file__).resolve().parents[2] / "fixtures" / "demo_sunglass_b.html"
DOMAIN = "demo-sunglass-b.example"

class DemoSunglassB(Connector):
    code = "demo_sunglass_b"
    name = "Demo Sunglass Shop B"

    def supports(self, url: str) -> bool:
        return urlparse(url).netloc.lower() == DOMAIN

    def fetch_offers(self, urls):
        wanted = set(urls)
        tree = HTMLParser(FIXTURE.read_text(encoding="utf-8"))
        offers = []
        for row in tree.css("tr.offer"):
            href = row.css_first("a").attributes.get("href")
            if href not in wanted:
                continue
            title = row.css_first("td.title").text(strip=True)
            brand = row.css_first("td.brand").text(strip=True)
            model_code = row.css_first("td.model_code").text(strip=True)
            color = row.css_first("td.color").text(strip=True)
            size = row.css_first("td.size").text(strip=True)
            price = float(row.css_first("td.price").text(strip=True).replace("EUR", "").strip())
            shipping = float(row.css_first("td.shipping").text(strip=True).replace("EUR", "").strip())
            tax = float(row.css_first("td.tax").text(strip=True).replace("EUR", "").strip())
            fee = float(row.css_first("td.fee").text(strip=True).replace("EUR", "").strip())
            offers.append(OfferIn(
                site_code=self.code, product_type="sunglass", url=href, title_raw=title,
                brand=brand, identifiers={"model_code": model_code, "color": color, "size": size},
                currency="EUR", base_price=price, shipping_cost=shipping, tax_estimate=tax, payment_fee=fee,
                coupon_value=0.0, cashback_value=0.0, availability="in_stock",
                seller_rating=4.4, delivery_days=6
            ))
        return offers
