from fastapi import FastAPI
from .routers.lead_scoring import router as lead_scoring_router
from .config.config import get_settings


# Create the FastAPI instance
app = FastAPI(
    title="MLFlow FastAPI Backend",
    description="A minimal FastAPI app for ML model serving and API endpoints",
    version="1.0.0"
)

# Router registration
app.include_router(lead_scoring_router)

if __name__ == "__main__":
    import uvicorn

    # 👇 Leer configuración desde Pydantic Settings
    settings = get_settings()

    # Mostrar valores cargados (útil para debug)
    print(f"Starting server at {settings.api.host}:{settings.api.port} (debug={settings.app.debug})")

    uvicorn.run(
        "backend.app.main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.app.debug,  # reload solo si debug=True
        env_file="backend/.env",     # opcional, refuerza la carga del .env
    )
