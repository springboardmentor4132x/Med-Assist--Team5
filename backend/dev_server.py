"""LOCAL DEMO SERVER ONLY.

Lets you run and test Risk Categorization on its own. In the real project,
do NOT use this file: Member 5 should instead add to the existing FastAPI app:

    from risk_categorization.router import router as risk_categorization_router
    app.include_router(risk_categorization_router)

Run (from the backend/ folder):  uvicorn dev_server:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from risk_categorization.router import router

app = FastAPI(title="MedAssist AI - Risk Categorization (dev)")

# Open CORS is for local development only. Restrict origins in production.
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
