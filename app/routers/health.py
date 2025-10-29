"""
Health check endpoints for monitoring and diagnostics.
"""

from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def basic_health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "MLFlow FastAPI Backend",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
