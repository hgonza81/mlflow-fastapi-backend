# MLFlow FastAPI Backend

A minimal FastAPI application for serving ML models and API endpoints, featuring lead scoring functionality.

## 🚀 Features

- **FastAPI**: Modern, fast web framework for building APIs
- **Lead Scoring**: Endpoint for calculating lead scores
- **Health Check**: Monitoring endpoint to verify service status
- **Docker**: Complete containerization setup
- **Environment Configuration**: Using Pydantic Settings
- **Local Development**: Full support for development with hot-reload

## 📋 Requirements

- **Docker & Docker Compose** (recommended - works out of the box)
- **Python 3.11+** (optional - for local development)
- **Make** (for unified command interface)

## 🛠️ Quick Start

### Option 1: Complete Setup (Recommended)
```bash
# Clone and setup everything
git clone <repository-url>
cd <project-directory>
cp .env.example .env

# Complete development setup
make dev-setup

# Start development environment
make dev
```

### Option 2: Docker Only
```bash
# Clone repository
git clone <repository-url>
cd <project-directory>
cp .env.example .env

# Start directly with Docker
make dev
```

### Option 3: Local Development
```bash
# Setup local environment
make install
make dev
```

## 🚀 Running the Application

### Development Mode (Hot Reload)
```bash
make dev                    # Start with hot reload
```

### Production Mode
```bash
make prod                   # Start in background
```

### Check Application Status
```bash
make status                 # View service status
make health                 # Quick health check
make logs                   # View application logs
```

### Stop Application
```bash
make stop                   # or make down
```

## 🧪 Testing

The project includes comprehensive unit tests with **98% code coverage** and intelligent environment detection.

### Quick Testing Commands

```bash
# Fast Development Testing
make test                    # Quick tests (no coverage)
make test-watch             # Watch mode for TDD

# Comprehensive Testing  
make test-local             # Local tests with coverage
make test-coverage          # Smart: local or Docker with coverage
make test-docker            # Docker validation tests

# Specific Testing
make test-specific FILE=test_api.py    # Run specific test file

# Quality Assurance
make validate               # Full validation before commit
make clean                  # Clean test artifacts and cache
```

### Intelligent Environment Detection

The testing system automatically detects your environment:
- **Python available locally** → Runs tests locally (faster)
- **No local Python** → Automatically uses Docker (consistent)
- **Coverage reports** → Generated in both HTML and terminal formats

## 📋 Available Commands

### Application Commands
```bash
make dev                    # Start development environment with hot reload
make prod                   # Start production environment in background
make stop                   # Stop all services (alias: make down)
make restart                # Restart all services
make logs                   # Show API logs
make build                  # Build Docker image
make status                 # Show service status
make health                 # Quick health check
```

### Testing Commands
```bash
make test                   # Run tests locally (default/fast)
make test-local             # Run tests locally with coverage
make test-docker            # Run tests in Docker (validation)
make test-coverage          # Run tests with coverage report
make test-watch             # Run tests in watch mode
make test-specific FILE=test_name.py  # Run specific test
```

### Utility Commands
```bash
make install                # Install dependencies locally
make clean                  # Clean test artifacts and cache
make validate               # Full validation before commit
make dev-setup              # Complete development environment setup
make help                   # Show all available commands
```

## 🏗️ Project Structure

```
├── app/
│   ├── config/             # Configuration management
│   ├── core/               # Core functionality (logging, exceptions)
│   ├── routers/            # API route handlers
│   └── schemas/            # Pydantic data models
├── tests/                  # Comprehensive test suite (98% coverage)
├── docker-compose.yml      # Application orchestration
├── docker-compose.test.yml # Testing environment
├── Dockerfile              # Application container
├── Makefile               # Unified command interface
└── requirements.txt       # Python dependencies
```

## 🔧 Development Workflow

### Daily Development
```bash
make dev                    # Start development
make test-watch             # Run tests in watch mode
make health                 # Verify everything works
```

### Before Committing
```bash
make validate               # Run full validation
# This runs: clean → test-coverage → test-docker
```

### First Time Setup
```bash
make dev-setup              # Complete setup
make dev                    # Start developing
```

## 🌐 API Endpoints

Once the application is running (via `make dev`), the API will be available at `http://localhost:8000`

### Health Check
```bash
# Basic health check
curl http://localhost:8000/health

# Detailed health check
curl http://localhost:8000/health/detailed
```

### Lead Scoring
```bash
# Score a lead
curl -X POST http://localhost:8000/lead-scoring/score \
  -H "Content-Type: application/json" \
  -d '{"lead_id": 123, "features": {"age": 30, "income": 50000}}'
```

### Interactive API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔍 Monitoring & Logging

The application includes comprehensive logging and monitoring:

- **Structured Logging**: JSON formatted logs with request IDs
- **Request/Response Tracking**: Automatic logging of all API calls
- **Error Handling**: Centralized exception handling with proper logging
- **Health Monitoring**: Built-in health check endpoints

### View Logs
```bash
make logs                   # View real-time application logs
```

## 🧪 Test Coverage

Current test coverage: **98%** 🎉

```bash
make test-coverage          # Generate coverage report
# View HTML report: open htmlcov/index.html
```