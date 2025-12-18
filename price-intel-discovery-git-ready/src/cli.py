from __future__ import annotations
import argparse
from rich import print
from src.db.session import SessionLocal
from src.connectors.registry import list_connectors
from src.product_types.registry import list_product_types
from src.discovery.registry import get_provider
from src.jobs.truth_crawl import run_truth_crawl
from src.jobs.discover_and_crawl import discover_and_crawl
from src.services.query import best_deal

def main():
    p = argparse.ArgumentParser(prog="price-intel-discovery")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("connectors")
    sub.add_parser("product-types")
    sub.add_parser("discovery-provider")

    p_discover = sub.add_parser("discover")
    p_discover.add_argument("--product-type", required=True, choices=list_product_types())
    p_discover.add_argument("--query", required=True)
    p_discover.add_argument("--max-results", type=int, default=10)

    p_dc = sub.add_parser("discover-and-crawl")
    p_dc.add_argument("--product-type", required=True, choices=list_product_types())
    p_dc.add_argument("--query", required=True)
    p_dc.add_argument("--max-results", type=int, default=10)

    p_tc = sub.add_parser("truth-crawl")
    p_tc.add_argument("--url", action="append", default=[], help="repeatable")

    p_best = sub.add_parser("best-deal")
    p_best.add_argument("--product-type", required=True, choices=list_product_types())
    p_best.add_argument("--key", required=True)

    args = p.parse_args()

    if args.cmd == "connectors":
        print(list_connectors()); return
    if args.cmd == "product-types":
        print(list_product_types()); return
    if args.cmd == "discovery-provider":
        print({"provider": get_provider().code}); return

    if args.cmd == "discover":
        provider = get_provider()
        urls = provider.discover_urls(args.query, max_results=args.max_results)
        print({"provider": provider.code, "query": args.query, "urls": urls}); return

    if args.cmd == "truth-crawl":
        if not args.url:
            print("[red]No URLs provided[/red]"); return
        with SessionLocal() as db:
            res = run_truth_crawl(db, args.url)
            db.commit()
            print(res); return

    if args.cmd == "discover-and-crawl":
        with SessionLocal() as db:
            res = discover_and_crawl(db, args.product_type, args.query, max_results=args.max_results)
            db.commit()
            print(res); return

    if args.cmd == "best-deal":
        with SessionLocal() as db:
            out = best_deal(db, args.product_type, args.key)
            if not out:
                print(f"[red]No deal found for[/red] {args.product_type}:{args.key}")
                return
            print(out.model_dump()); return

if __name__ == "__main__":
    main()
