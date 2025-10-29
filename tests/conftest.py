"""Pytest configuration and fixtures."""

import logging
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_request():
    """Create a mock FastAPI Request object."""
    request = Mock()
    request.method = "GET"
    request.url = "http://testserver/test"
    request.url.path = "/test"
    request.client.host = "127.0.0.1"
    request.headers.get.return_value = "test-user-agent"
    return request


@pytest.fixture
def mock_response():
    """Create a mock FastAPI Response object."""
    response = Mock()
    response.status_code = 200
    return response


@pytest.fixture(autouse=True)
def setup_test_logging():
    """Set up logging for tests."""
    # Disable logging during tests to avoid noise
    logging.disable(logging.CRITICAL)
    yield
    # Re-enable logging after tests
    logging.disable(logging.NOTSET)


@pytest.fixture
def sample_validation_errors():
    """Sample validation errors for testing."""
    return [
        {
            "field": "lead_id",
            "message": "field required",
            "type": "value_error.missing",
        },
        {
            "field": "email",
            "message": "invalid email format",
            "type": "value_error.email",
        },
    ]
