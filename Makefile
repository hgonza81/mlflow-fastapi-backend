.PHONY: help dev prod stop logs build test test-local test-docker test-coverage test-watch test-ci clean up down restart status validate

# Default target
help:
	@echo "🚀 MLFlow FastAPI Backend - Available Commands"
	@echo ""
	@echo "📱 Application Commands:"
	@echo "  dev            - Start development environment with hot reload"
	@echo "  prod           - Start production environment in background"
	@echo "  stop/down      - Stop all services"
	@echo "  logs           - Show API logs"
	@echo "  build          - Build Docker image"
	@echo "  restart        - Restart all services"
	@echo "  status         - Show service status"
	@echo ""
	@echo "🧪 Testing Commands:"
	@echo "  test           - Run tests locally (default/fast)"
	@echo "  test-local     - Run tests locally with coverage"
	@echo "  test-docker    - Run tests in Docker (validation)"
	@echo "  test-coverage  - Run tests with coverage report"
	@echo "  test-watch     - Run tests in watch mode"
	@echo "  test-specific  - Run specific test (FILE=test_name.py)"
	@echo ""
	@echo "🛠️  Utility Commands:"
	@echo "  clean          - Clean test artifacts and cache"
	@echo "  validate       - Full validation before commit"
	@echo "  install        - Install dependencies locally"

# Application commands
dev:
	@echo "🚀 Starting development environment..."
	docker compose up --build

prod:
	@echo "🚀 Starting production environment..."
	docker compose up --build -d

stop:
	@echo "🛑 Stopping all services..."
	docker compose down

logs:
	@echo "📋 Showing API logs..."
	docker compose logs -f api

build:
	@echo "🔨 Building Docker image..."
	docker compose build

# Local development tests (fast)
test:
	@echo "🚀 Running tests locally (fast)..."
	python -m pytest tests/ -v --tb=short

test-local:
	@echo "🚀 Running tests locally with coverage..."
	python -m pytest tests/ --cov=app --cov-report=html --cov-report=term-missing -v

# Docker tests (validation)
test-docker:
	@echo "🐳 Running tests in Docker..."
	docker compose -f docker-compose.test.yml run --rm test

test-coverage:
	@echo "📊 Running tests with coverage..."
	@if command -v python >/dev/null 2>&1; then \
		echo "🚀 Running locally..."; \
		python -m pytest tests/ --cov=app --cov-report=html --cov-report=term-missing -v; \
	else \
		echo "🐳 Running in Docker..."; \
		docker compose -f docker-compose.test.yml run --rm test-coverage; \
	fi

test-watch:
	@echo "👀 Running tests in watch mode..."
	@if command -v python >/dev/null 2>&1; then \
		echo "🚀 Running locally..."; \
		python -m pytest tests/ -v --tb=short -f; \
	else \
		echo "🐳 Running in Docker..."; \
		docker compose -f docker-compose.test.yml run --rm test-watch; \
	fi

# Specific test file
test-specific:
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Please specify FILE=test_filename.py"; \
		echo "   Example: make test-specific FILE=test_api.py"; \
		exit 1; \
	fi
	@echo "🎯 Running specific test: $(FILE)"
	@if command -v python >/dev/null 2>&1; then \
		python -m pytest tests/$(FILE) -v; \
	else \
		docker compose -f docker-compose.test.yml run --rm test python -m pytest tests/$(FILE) -v; \
	fi

# Build and maintenance
build-test:
	@echo "🔨 Building test Docker image..."
	docker compose -f docker-compose.test.yml build test

clean:
	@echo "🧹 Cleaning test artifacts and cache..."
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf test-results/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	docker system prune -f --volumes 2>/dev/null || true

# Install dependencies locally
install:
	@echo "📦 Installing dependencies locally..."
	@if command -v pip >/dev/null 2>&1; then \
		pip install -r requirements.txt; \
		pip install pytest pytest-cov pytest-asyncio httpx; \
	else \
		echo "❌ pip not found. Please install Python and pip first."; \
		exit 1; \
	fi

# Combined commands
up: dev

down: stop

restart:
	@echo "🔄 Restarting services..."
	make stop
	make dev

status:
	@echo "📊 Service status..."
	docker compose ps

# Full validation before commit
validate:
	@echo "🔍 Running full validation..."
	make clean
	make test-coverage
	make test-docker
	@echo "✅ Validation complete!"

# Development workflow
dev-setup:
	@echo "🛠️  Setting up development environment..."
	make install
	make build
	@echo "✅ Development setup complete! Run 'make dev' to start."

# Quick health check
health:
	@echo "🏥 Checking application health..."
	@if docker compose ps | grep -q "Up"; then \
		curl -s http://localhost:8000/health || echo "❌ Health check failed"; \
	else \
		echo "❌ Application not running. Use 'make dev' to start."; \
	fi