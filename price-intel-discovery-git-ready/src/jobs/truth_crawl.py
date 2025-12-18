from __future__ import annotations
from sqlalchemy.orm import Session
from src.connectors.registry import route_urls, get_connector_by_code
from src.services.persist import upsert_site, find_or_create_product, insert_offer

def run_truth_crawl(db: Session, urls: list[str]) -> dict:
    buckets = route_urls(urls)
    results = {"matched_connectors": buckets, "inserted_offers": 0, "skipped_urls": []}

    matched_urls = set()
    for _, ulist in buckets.items():
        matched_urls.update(ulist)
    results["skipped_urls"] = [u for u in urls if u not in matched_urls]

    for code, ulist in buckets.items():
        conn = get_connector_by_code(code)
        site = upsert_site(db, conn.code, conn.name)
        offers = conn.fetch_offers(ulist)
        for off in offers:
            product = find_or_create_product(db, off)
            insert_offer(db, site, product, off)
            results["inserted_offers"] += 1

    return results
