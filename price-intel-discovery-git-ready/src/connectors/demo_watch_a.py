from __future__ import annotations
from pathlib import Path
from urllib.parse import urlparse
from selectolax.parser import HTMLParser
from src.connectors.base import Connector
from src.core.types import OfferIn

FIXTURE = Path(__file__).resolve().parents[2] / "fixtures" / "demo_watch_a.html"
DOMAIN = "demo-watch-a.example"

class DemoWatchA(Connector):
    code = "demo_watch_a"
    name = "Demo Watch Market A"

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
            reference = card.css_first(".reference").text(strip=True)
            price = float(card.css_first(".price").text(strip=True).replace("€", "").strip())
            shipping = float(card.css_first(".shipping").text(strip=True).replace("€", "").strip())
            rating = float(card.css_first(".rating").text(strip=True))
            delivery = int(card.css_first(".delivery_days").text(strip=True))
            offers.append(OfferIn(
                site_code=self.code, product_type="watch", url=href, title_raw=title,
                identifiers={"reference": reference}, currency="EUR",
                base_price=price, shipping_cost=shipping, tax_estimate=0.0, payment_fee=0.0,
                coupon_value=0.0, cashback_value=0.0, availability="in_stock",
                seller_rating=rating, delivery_days=delivery
            ))
        return offers
