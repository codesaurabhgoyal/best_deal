from __future__ import annotations
from typing import Dict
from src.product_types.base import ProductTypeStrategy
from src.product_types.watch import WatchStrategy
from src.product_types.sunglass import SunglassStrategy

_REG: Dict[str, ProductTypeStrategy] = {
    "watch": WatchStrategy(),
    "sunglass": SunglassStrategy(),
}

def get_strategy(product_type: str) -> ProductTypeStrategy:
    pt = (product_type or "").strip().lower()
    if pt not in _REG:
        raise KeyError(f"Unknown product_type '{product_type}'. Available: {list(_REG)}")
    return _REG[pt]

def list_product_types() -> list[str]:
    return list(_REG.keys())
