from __future__ import annotations
from pydantic import BaseModel
from dotenv import load_dotenv
import os
load_dotenv()

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./price_intel.db")

    enable_scheduler: bool = os.getenv("ENABLE_SCHEDULER", "false").lower() == "true"
    crawl_interval_minutes: int = int(os.getenv("CRAWL_INTERVAL_MINUTES", "360"))

    weight_price: float = float(os.getenv("WEIGHT_PRICE", "1.0"))
    weight_delivery_days: float = float(os.getenv("WEIGHT_DELIVERY_DAYS", "0.02"))
    weight_seller_rating: float = float(os.getenv("WEIGHT_SELLER_RATING", "0.5"))

    discovery_provider: str = os.getenv("DISCOVERY_PROVIDER", "demo").lower()
    bing_api_key: str | None = os.getenv("BING_API_KEY") or None
    bing_endpoint: str = os.getenv("BING_ENDPOINT", "https://api.bing.microsoft.com/v7.0/search")

    google_cse_api_key: str | None = os.getenv("GOOGLE_CSE_API_KEY") or None
    google_cse_cx: str | None = os.getenv("GOOGLE_CSE_CX") or None

settings = Settings()
