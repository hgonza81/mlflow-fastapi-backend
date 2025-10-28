from pydantic import BaseModel
from typing import Dict

class LeadScoringRequest(BaseModel):
    lead_id: int
    features: Dict[str, float]
