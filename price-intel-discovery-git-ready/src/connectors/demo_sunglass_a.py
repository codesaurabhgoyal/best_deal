from __future__ import annotations
from pathlib import Path
from urllib.parse import urlparse
from selectolax.parser import HTMLParser
from src.connectors.base import Connector
from src.core.types import OfferIn

FIXTURE = Path(__file__).resolve().parents[2] / "fixtures" / "demo_sunglass_a.html"
DOMAIN = "demo-sunglass-a.example"

class DemoSunglassA(Connector):
    code = "demo_sunglass_a"
    name = "Demo Sunglass Shop A"

    def supports(self, url: str) -> bool:
        return urlparse(url).netloc.lower() == DOMAIN

    def fetch_offers(self, urls):
        wanted = set(urls)
        tree = HTMLParser(FIXTURE.read_text(encoding="utf-8"))
        offers = []
        for card in tree.css(".card"):
            href = card.css_first("a").attributes.get("href")
            if href not in wanted:
                continue
            title = card.css_first(".title").text(strip=True)
            brand = card.css_first(".brand").text(strip=True)
            model_code = card.css_first(".model_code").text(strip=True)
            gtin = card.css_first(".gtin").text(strip=True)
            color = card.css_first(".color").text(strip=True)
            size = card.css_first(".size").text(strip=True)
            price = float(card.css_first(".price").text(strip=True).replace("€", "").strip())
            shipping = float(card.css_first(".shipping").text(strip=True).replace("€", "").strip())
            coupon = float(card.css_first(".coupon").text(strip=True).replace("€", "").strip())
            cashback = float(card.css_first(".cashback").text(strip=True).replace("€", "").strip())
            offers.append(OfferIn(
                site_code=self.code, product_type="sunglass", url=href, title_raw=title,
                brand=brand, identifiers={"gtin": gtin, "model_code": model_code, "color": color, "size": size},
                currency="EUR", base_price=price, shipping_cost=shipping, tax_estimate=0.0, payment_fee=0.0,
                coupon_value=coupon, cashback_value=cashback, availability="in_stock",
                seller_rating=4.7, delivery_days=4
            ))
        return offers
