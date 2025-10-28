#!/bin/bash

# MLFlow FastAPI Backend Docker Runner

case "$1" in
    "dev")
        echo "Starting development environment..."
        docker compose up --build
        ;;
    "prod")
        echo "Starting production environment..."
        docker compose up --build -d
        ;;
    "stop")
        echo "Stopping all services..."
        docker compose down
        ;;
    "logs")
        echo "Showing logs..."
        docker compose logs -f api
        ;;
    "build")
        echo "Building image..."
        docker compose build
        ;;
    *)
        echo "Usage: $0 {dev|prod|stop|logs|build}"
        echo ""
        echo "Commands:"
        echo "  dev   - Start development environment with hot reload"
        echo "  prod  - Start production environment in background"
        echo "  stop  - Stop all services"
        echo "  logs  - Show API logs"
        echo "  build - Build Docker image"
        exit 1
        ;;
esac