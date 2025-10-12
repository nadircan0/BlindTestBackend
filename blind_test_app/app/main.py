from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers import api_router
from app.db import base
from app.db.session import engine

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "scopes": {}
    }
)

# CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    origins = [origin.strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    """Ana sayfa"""
    return {"message": "Blind Test Backend API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    """Health check"""
    return {"status": "healthy"}

