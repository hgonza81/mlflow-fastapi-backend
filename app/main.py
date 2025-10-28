"""
MLFlow FastAPI Backend - Main Application Module

This module contains the main FastAPI application instance and configuration.
It sets up the API routes, health checks, and server startup configuration
using Pydantic Settings for environment-based configuration management.
"""

from fastapi import FastAPI
from .routers.lead_scoring import router as lead_scoring_router

# Create the FastAPI instance
app = FastAPI(
    title="MLFlow FastAPI Backend",
    description="A minimal FastAPI app for ML model serving and API endpoints",
    version="1.0.0"
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring service availability.
    
    Returns:
        dict: Status information including service health and name
    """
    return {"status": "healthy", "service": "MLFlow FastAPI Backend"}

# Router registration
app.include_router(lead_scoring_router)
