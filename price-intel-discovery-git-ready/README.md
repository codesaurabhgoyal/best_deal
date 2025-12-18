# Price Intelligence: Discovery (Search API) + Truth (Merchant Extraction)

Goal: “Go online and find the best deal anywhere.”

Directly scraping Google/Bing result pages is fragile + ToS-problematic, so this repo implements the **professional approach**:

1) **Discovery layer (API-based search)** → finds candidate seller URLs across the web  
2) **Truth layer (connectors)** → visits seller pages and computes **real total price**

✅ **True total (what you actually pay)**:
`total = base_price + shipping + tax + payment_fee - coupon_value - cashback_value`

---

## Architecture

```
Query / Product ID
   |
   v
[Discovery Provider]  (Bing API / Google CSE / Demo)
   |
   v
Candidate URLs (many domains)
   |
   v
[Connector Router] -> (Connector per domain/site)
   |
   v
Offers (normalized) -> TRUE TOTAL -> DB history
   |
   v
Best Deal API / CLI
```

---

## Quick start (demo mode)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
alembic upgrade head
```

### Discover
```bash
python -m src.cli discover --product-type watch --query "Rolex 116610LN"
```

### Discover + truth crawl
```bash
python -m src.cli discover-and-crawl --product-type watch --query "Rolex 116610LN"
python -m src.cli best-deal --product-type watch --key 116610LN
```

### API
```bash
uvicorn src.api.app:app --reload
# http://127.0.0.1:8000/docs
```

---

## Switch to real discovery

### Bing Web Search API
Set in .env:
- DISCOVERY_PROVIDER=bing
- BING_API_KEY=...

### Google Programmable Search (CSE JSON API)
Set in .env:
- DISCOVERY_PROVIDER=google_cse
- GOOGLE_CSE_API_KEY=...
- GOOGLE_CSE_CX=...

## Author

**Saurabh Goyal**  
Senior Product & AI Consultant | Data, Cloud, AI Systems  
📍 Germany / Europe (Remote)

- LinkedIn: https://www.linkedin.com/in/saurabh-product-tech-strategy/
- GitHub: https://github.com/codesaurabhgoyal

