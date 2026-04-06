from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import catalogo_musicas, ciclos, dashboard, eventos, frequencias, health, inicio, musicas, pessoas, trimestres
from app.core.config import settings
from app.services.files_service import ensure_upload_dir


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix=settings.api_prefix)
    app.include_router(pessoas.router, prefix=settings.api_prefix)
    app.include_router(ciclos.router, prefix=settings.api_prefix)
    app.include_router(trimestres.router, prefix=settings.api_prefix)
    app.include_router(eventos.router, prefix=settings.api_prefix)
    app.include_router(musicas.router, prefix=settings.api_prefix)
    app.include_router(catalogo_musicas.router, prefix=settings.api_prefix)
    app.include_router(frequencias.router, prefix=settings.api_prefix)
    app.include_router(dashboard.router, prefix=settings.api_prefix)
    app.include_router(inicio.router, prefix=settings.api_prefix)

    @app.on_event("startup")
    def _startup() -> None:
        ensure_upload_dir()

    return app


app = create_app()
