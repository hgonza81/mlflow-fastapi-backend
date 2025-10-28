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

- Python 3.11+
- Docker and Docker Compose (optional, for container-based development)

## 🛠️ Local Development Environment Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```
1. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit the .env file with your configurations
   ```
1. **Build and run with Docker Compose**

   ```bash
   docker-compose up --build
   ```
1. **For development with hot-reload, ensure in your .env:**

   ```
   APP_DEBUG=true
   ```