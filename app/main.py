"""
MLFlow FastAPI Backend - Main Application Module

This module contains the main FastAPI application instance and configuration.
It sets up the API routes, health checks, and server startup configuration
using Pydantic Settings for environment-based configuration management.
"""

from fastapi import FastAPI
from .core.logging import configure_logging, LoggingMiddleware
from .core.exceptions import register_exception_handlers
from .routers.health import router as health_router
from .routers.lead_scoring import router as lead_scoring_router

configure_logging()

# Create the FastAPI instance
app = FastAPI(
    title="MLFlow FastAPI Backend",
    description="A minimal FastAPI app for ML model serving and API endpoints",
    version="1.0.0",
)

# Exception Handlers
register_exception_handlers(app)

# Middleware
app.add_middleware(LoggingMiddleware)

# Routers
app.include_router(health_router)
app.include_router(lead_scoring_router)
