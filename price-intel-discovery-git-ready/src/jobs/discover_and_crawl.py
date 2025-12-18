from __future__ import annotations
from sqlalchemy.orm import Session
from src.discovery.registry import get_provider
from src.jobs.truth_crawl import run_truth_crawl

def discover_and_crawl(db: Session, product_type: str, query: str, max_results: int = 10) -> dict:
    provider = get_provider()
    urls = provider.discover_urls(query=query, max_results=max_results)
    crawl_res = run_truth_crawl(db, urls)
    return {"discovery_provider": provider.code, "query": query, "discovered_urls": urls, "truth_crawl": crawl_res}
