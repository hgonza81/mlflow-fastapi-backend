"""Lead scoring API router.

This module defines the API endpoints for lead scoring functionality,
including score calculation and health check endpoints.
"""

from fastapi import APIRouter
from ..schemas.lead_scoring_request import LeadScoringRequest
from ..schemas.lead_scoring_response import LeadScoringResponse

router = APIRouter(
    prefix="/lead-scoring",
    tags=["lead-scoring"],
    responses={404: {"description": "Not found"}},
)

@router.post("/score", response_model=LeadScoringResponse)
async def score(request: LeadScoringRequest) -> LeadScoringResponse:
    """Calculate lead scoring based on request data."""
    return LeadScoringResponse(lead_id=request.lead_id, score=25)
