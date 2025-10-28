from pydantic import BaseModel

class LeadScoringResponse(BaseModel):
    lead_id: int
    score: float
