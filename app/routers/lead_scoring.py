from typing import Any, Coroutine

from fastapi import APIRouter
from backend.app.schemas.lead_scoring_request import LeadScoringRequest
from backend.app.schemas.lead_scoring_response import LeadScoringResponse

# Create router with prefix and tags
router = APIRouter(
    prefix="/lead-scoring",
    tags=["lead-scoring"],
    responses={404: {"description": "Not found"}},
)

@router.post("/score", response_model=LeadScoringResponse)
async def score(request: LeadScoringRequest) -> LeadScoringResponse:
    return LeadScoringResponse(lead_id=request.lead_id, score=25)

@router.get("/live")
async def health():
    return {"status": "ok"}

@router.get("/ready")
async def ready():
    return {"status": "ok"}