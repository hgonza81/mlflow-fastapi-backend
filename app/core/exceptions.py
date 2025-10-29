"""
Exception handlers for the FastAPI application.

This module contains custom exception handlers that provide consistent
error responses and logging for different types of application errors.
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .logging import error_logger


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed logging.

    Args:
        request: The FastAPI request object
        exc: The validation exception that occurred

    Returns:
        JSONResponse with validation error details
    """
    request_id = request.headers.get("x-request-id", "unknown")

    error_logger.log_validation_error(
        request=request, request_id=request_id, errors=exc.errors()
    )

    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "Request validation failed",
            "details": exc.errors(),
            "request_id": request_id,
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with appropriate logging.

    Args:
        request: The FastAPI request object
        exc: The HTTP exception that occurred

    Returns:
        JSONResponse with HTTP error details
    """
    request_id = request.headers.get("x-request-id", "unknown")

    error_logger.log_http_error(
        request=request,
        request_id=request_id,
        status_code=exc.status_code,
        detail=exc.detail,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "message": exc.detail,
            "request_id": request_id,
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions with logging.

    Args:
        request: The FastAPI request object
        exc: The exception that occurred

    Returns:
        JSONResponse with generic error message
    """
    request_id = request.headers.get("x-request-id", "unknown")

    error_logger.log_internal_error(request=request, request_id=request_id, error=exc)

    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": "An internal server error occurred",
            "request_id": request_id,
        },
    )


def register_exception_handlers(app):
    """Register all exception handlers with the FastAPI app.

    Args:
        app: The FastAPI application instance
    """
    # Order matters: more specific handlers first
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
