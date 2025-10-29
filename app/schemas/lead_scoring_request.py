"""Lead scoring request schema definitions."""

from typing import Dict
from pydantic import BaseModel


class LeadScoringRequest(BaseModel):
    """Request model for lead scoring API endpoint.

    Attributes:
        lead_id: Unique identifier for the lead
        features: Dictionary of feature names and their values for scoring
    """

    lead_id: int
    features: Dict[str, float]
