"""Healthcheck endpoint: a liveness signal for orchestrators and smoke tests."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from pattern_specular import __version__
from pattern_specular.core.config import Settings, get_settings

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Service health payload returned by the healthcheck."""

    status: Literal["ok"]
    app_env: str
    version: str


@router.get("/health", response_model=HealthResponse, summary="Liveness healthcheck")
def healthcheck(settings: Annotated[Settings, Depends(get_settings)]) -> HealthResponse:
    """Report that the service is up, with its running environment and version."""
    return HealthResponse(status="ok", app_env=settings.app_env, version=__version__)


class ReadyResponse(BaseModel):
    """Readiness payload indicating database connectivity."""

    status: Literal["ok"]
    database: Literal["connected"]
    app_env: str


@router.get("/health/ready", response_model=ReadyResponse, summary="Readiness probe")
def readiness(settings: Annotated[Settings, Depends(get_settings)]) -> ReadyResponse:
    """Verify database connectivity as an infrastructure readiness probe."""
    from sqlalchemy import text
    from pattern_specular.db.session import get_sessionmaker

    with get_sessionmaker()() as session:
        session.execute(text("SELECT 1"))
    return ReadyResponse(status="ok", database="connected", app_env=settings.app_env)
