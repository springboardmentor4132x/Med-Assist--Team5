"""FastAPI router for Member 5 to include in the existing app:

    from risk_categorization.router import router as risk_categorization_router
    app.include_router(risk_categorization_router)

Invalid payloads return HTTP 422 automatically. If the project protects routes,
add its auth dependency, e.g. APIRouter(..., dependencies=[Depends(get_current_user)]).
"""
from fastapi import APIRouter

from .schemas import RiskCategorizationInput, RiskCategorizationResult
from .service import categorize_risk

router = APIRouter(prefix="/api/risk", tags=["Risk Categorization"])


@router.post("/categorization", response_model=RiskCategorizationResult, status_code=200)
def categorize(payload: RiskCategorizationInput) -> RiskCategorizationResult:
    return categorize_risk(payload)
