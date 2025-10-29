"""
Logging utilities and configuration for the FastAPI application.

This module provides structured logging capabilities, error tracking,
and request/response logging middleware for comprehensive application monitoring.
"""

import logging
import json
import uuid
from datetime import datetime, timezone
import time
from fastapi import Request, Response


class StructuredLogger:
    """Structured logging utility for consistent log formatting."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def log_request(self, request: Request, request_id: str, start_time: float):
        """Log incoming request details."""
        log_data = {
            "event": "request_received",
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "start_time": start_time,
        }
        self.logger.info(json.dumps(log_data))

    def log_response(
        self,
        request: Request,
        response: Response,
        request_id: str,
        start_time: float,
        end_time: float,
    ):
        """Log response details."""
        duration = end_time - start_time
        log_data = {
            "event": "request_completed",
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.logger.info(json.dumps(log_data))


class ErrorLogger:
    """Specialized logger for exception handling logging."""

    def __init__(self):
        self.validation_logger = logging.getLogger("validation_errors")
        self.internal_logger = logging.getLogger("internal_errors")
        self.http_logger = logging.getLogger("http_errors")

    def log_validation_error(self, request: Request, request_id: str, errors: list):
        """Log validation errors with detailed context."""
        log_data = {
            "event": "validation_error",
            "request_id": request_id,
            "method": request.method,
            "path": str(request.url.path),
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
            "errors": errors,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.validation_logger.warning(json.dumps(log_data))

    def log_internal_error(self, request: Request, request_id: str, error: Exception):
        """Log internal server errors."""
        log_data = {
            "event": "internal_error",
            "request_id": request_id,
            "method": request.method,
            "path": str(request.url.path),
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.internal_logger.error(json.dumps(log_data), exc_info=True)

    def log_http_error(
        self, request: Request, request_id: str, status_code: int, detail: str
    ):
        """Log HTTP errors (4xx/5xx)."""
        log_data = {
            "event": "http_error",
            "request_id": request_id,
            "method": request.method,
            "path": str(request.url.path),
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
            "status_code": status_code,
            "error_detail": detail,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        # Log as error for 5xx, warning for 4xx
        if status_code >= 500:
            self.http_logger.error(json.dumps(log_data))
        else:
            self.http_logger.warning(json.dumps(log_data))


class LoggingMiddleware:
    """Middleware for comprehensive request/response logging."""

    def __init__(self, app):
        self.app = app
        self.logger = StructuredLogger("request_logger")

    async def __call__(self, scope, receive, send):
        """ASGI middleware for request/response logging."""

        # Skip logging for non-HTTP requests (e.g., WebSocket connections)
        # Only HTTP and HTTPS requests should be processed by this logging middleware
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        request_id = str(uuid.uuid4())
        start_time = time.time()

        # Add request ID to headers for tracking
        scope["headers"] = list(scope.get("headers", []))
        scope["headers"].append((b"x-request-id", request_id.encode()))

        # Log incoming request
        self.logger.log_request(request, request_id, start_time)

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                # Create response object for logging
                response = Response()
                response.status_code = message["status"]

                end_time = time.time()
                self.logger.log_response(
                    request, response, request_id, start_time, end_time
                )

            await send(message)

        # Let exceptions propagate to FastAPI exception handlers
        await self.app(scope, receive, send_wrapper)


def configure_logging(level: str = "INFO"):
    """Configure logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
        force=True,
    )

    # Set specific loggers to appropriate levels
    logging.getLogger("request_logger").setLevel(logging.INFO)
    logging.getLogger("validation_errors").setLevel(logging.WARNING)
    logging.getLogger("internal_errors").setLevel(logging.ERROR)
    logging.getLogger("http_errors").setLevel(logging.WARNING)

    logging.getLogger(__name__).info("Logging configured successfully")


# Global error logger instance
error_logger = ErrorLogger()
