# OmniPay — Payment Observability Prototype

OmniPay generates synthetic payments and displays them in a React dashboard. When a payment fails, a FastAPI background task asks Gemini to explain a randomly selected synthetic failure log and suggest a troubleshooting action.

## What is implemented

- Synthetic transactions generated every 2–5 seconds, with a simulated 30% failure rate.
- FastAPI endpoints for recent transactions and completed analyses.
- React dashboard polling transactions every two seconds.
- Optional Gemini analysis using a non-blocking async API call.
- Docker Compose for local development; GitHub Actions runs backend tests, Python lint checks, frontend builds and container builds.

## Scope and limitations

Transactions and analyses are held in memory and lost on restart. There is no log retrieval, embedding index or RAG pipeline. PostgreSQL and MongoDB containers in Compose are placeholders; the backend does not read or write them. Confidence is not measured and the API returns `null` rather than a fabricated score. There is no throughput benchmark, calibrated diagnostic accuracy or production deployment claim.

## Run locally

```bash
git clone https://github.com/AryanAI0035/payment-observability-engine.git
cd payment-observability-engine
export GEMINI_API_KEY="your_api_key"
# Optionally set GEMINI_MODEL to a model available to your account.
docker compose up --build
```

Dashboard: http://localhost:5173. API documentation: http://localhost:8000/docs.
Without an API key, transactions still run but analysis is disabled. Model availability depends on your Gemini account; the default model identifier is recorded in `backend/main.py`.

## Tests

```bash
python -m pip install -r backend/requirements.txt pytest
python -m pytest backend/tests -q
```

Tests mock Gemini; no API key or paid request is required.

## License

MIT License
