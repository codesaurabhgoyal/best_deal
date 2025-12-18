from __future__ import annotations
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.session import get_session
from src.connectors.registry import list_connectors
from src.product_types.registry import list_product_types
from src.discovery.registry import get_provider
from src.jobs.discover_and_crawl import discover_and_crawl
from src.jobs.truth_crawl import run_truth_crawl
from src.services.query import best_deal

app = FastAPI(title="Price Intelligence (Discovery + Truth)", version="0.3.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/connectors")
def connectors():
    return list_connectors()

@app.get("/product-types")
def product_types():
    return list_product_types()

@app.get("/discovery-provider")
def discovery_provider():
    return {"provider": get_provider().code}

@app.post("/discover")
def discover(payload: dict):
    provider = get_provider()
    query = payload.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Missing 'query'")
    max_results = int(payload.get("max_results") or 10)
    return {"provider": provider.code, "query": query, "urls": provider.discover_urls(query, max_results=max_results)}

@app.post("/truth-crawl")
def truth_crawl(payload: dict, db: Session = Depends(get_session)):
    urls = payload.get("urls") or []
    if not urls:
        raise HTTPException(status_code=400, detail="Missing 'urls' list")
    res = run_truth_crawl(db, urls)
    db.commit()
    return res

@app.post("/discover-and-crawl")
def discover_crawl(payload: dict, db: Session = Depends(get_session)):
    product_type = (payload.get("product_type") or "").lower()
    query = payload.get("query")
    if not product_type or not query:
        raise HTTPException(status_code=400, detail="Need 'product_type' and 'query'")
    max_results = int(payload.get("max_results") or 10)
    res = discover_and_crawl(db, product_type, query, max_results=max_results)
    db.commit()
    return res

@app.get("/best-deal/{product_type}/{identity_key}")
def best_deal_api(product_type: str, identity_key: str, db: Session = Depends(get_session)):
    out = best_deal(db, product_type.lower(), identity_key)
    if not out:
        raise HTTPException(status_code=404, detail="No offers found for this product key.")
    return out.model_dump()
