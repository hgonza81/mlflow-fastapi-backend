"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client fixture."""
    return TestClient(app)


@pytest.fixture
def valid_lead_payload():
    """Valid lead scoring payload fixture."""
    return {
        "lead_id": 1234,
        "features": {"age": 30.0, "income": 50000.0, "experience": 5.0},
    }


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_basic_health_check(self, client):
        """Test basic health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200, "Health check should return 200"
        data = response.json()
        assert data["status"] == "healthy", "Status should be healthy"
        assert data["service"] == "MLFlow FastAPI Backend", "Service name should match"
        assert "timestamp" in data, "Response should include timestamp"


class TestLeadScoringEndpoints:
    """Test lead scoring endpoints."""

    def test_lead_scoring_success(self, client, valid_lead_payload):
        """Test successful lead scoring."""
        response = client.post("/lead-scoring/score", json=valid_lead_payload)

        assert response.status_code == 200, "Valid request should return 200"
        data = response.json()
        assert (
            data["lead_id"] == valid_lead_payload["lead_id"]
        ), "Lead ID should match request"
        assert data["score"] == 25, "Score should be returned"
        assert isinstance(data["score"], (int, float)), "Score should be numeric"

    @pytest.mark.parametrize(
        "invalid_payload,expected_error",
        [
            ({}, "missing lead_id and features"),
            ({"lead_id": 123}, "missing features"),
            ({"features": {"age": 30.0}}, "missing lead_id"),
            ({"lead_id": "invalid", "features": {"age": 30.0}}, "invalid lead_id type"),
            ({"lead_id": 123, "features": "invalid"}, "invalid features type"),
        ],
    )
    def test_lead_scoring_validation_errors(
        self, client, invalid_payload, expected_error
    ):
        """Test various validation error scenarios."""
        response = client.post("/lead-scoring/score", json=invalid_payload)

        assert response.status_code == 422, f"Should return 422 for {expected_error}"
        data = response.json()
        assert "validation_error" in data["error"], "Should contain validation_error"
        assert "request_id" in data, "Should include request_id for tracking"

    def test_lead_scoring_invalid_json(self, client):
        """Test lead scoring with malformed JSON."""
        response = client.post(
            "/lead-scoring/score",
            content="invalid json",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 422, "Malformed JSON should return 422"

    def test_lead_scoring_edge_cases(self, client):
        """Test edge cases for lead scoring."""
        edge_cases = [
            # Very large lead_id
            {"lead_id": 999999999, "features": {"age": 25.0}},
            # Negative values in features
            {"lead_id": 123, "features": {"age": -5.0, "debt": 1000.0}},
            # Zero values
            {"lead_id": 123, "features": {"age": 0.0, "income": 0.0}},
        ]

        for payload in edge_cases:
            response = client.post("/lead-scoring/score", json=payload)
            # Should either succeed or fail gracefully
            assert response.status_code in [
                200,
                422,
            ], f"Edge case should handle gracefully: {payload}"


class TestAPIIntegration:
    """Test API integration and error handling."""

    def test_request_id_tracking(self, client):
        """Test that request ID is included in error responses."""
        response = client.post("/lead-scoring/score", json={})

        assert response.status_code == 422, "Invalid request should return 422"
        data = response.json()
        assert (
            "request_id" in data
        ), "Error response should include request_id for tracking"

    def test_nonexistent_endpoint(self, client):
        """Test 404 handling for nonexistent endpoints."""
        response = client.get("/nonexistent-endpoint")

        assert response.status_code == 404, "Nonexistent endpoint should return 404"

    def test_method_not_allowed(self, client):
        """Test 405 handling for wrong HTTP methods."""
        response = client.get("/lead-scoring/score")  # Should be POST

        assert response.status_code == 405, "Wrong HTTP method should return 405"

    def test_content_type_validation(self, client, valid_lead_payload):
        """Test that API validates content type properly."""
        # Test without content-type header
        response = client.post("/lead-scoring/score", content=str(valid_lead_payload))

        assert response.status_code in [
            400,
            422,
        ], "Missing content-type should be handled"
