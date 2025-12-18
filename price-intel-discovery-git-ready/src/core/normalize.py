from __future__ import annotations
import re

def normalize_title(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^a-z0-9\.\-\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def compute_total(base: float, shipping: float, tax: float, fee: float, coupon: float, cashback: float) -> float:
    return round((base + shipping + tax + fee - coupon - cashback), 2)
