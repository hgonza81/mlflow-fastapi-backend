"""Lead scoring response schema definitions."""

from pydantic import BaseModel


class LeadScoringResponse(BaseModel):
    """Response model for lead scoring API endpoint.

    Attributes:
        lead_id: Unique identifier for the lead that was scored
        score: Calculated lead score (typically between 0-100)
    """

    lead_id: int
    score: float
