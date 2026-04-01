from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.dashboard import DashboardCoralistaItemOut, DashboardNaipeItemOut, DashboardResumoOut
from app.services.dashboard_service import dashboard_coralistas, dashboard_naipes, dashboard_resumo

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/resumo", response_model=DashboardResumoOut)
def resumo_dashboard(
    ano: int | None = Query(default=None),
    trimestre: int | None = Query(default=None, ge=1, le=4),
    db: Session = Depends(get_db),
) -> DashboardResumoOut:
    return dashboard_resumo(db, ano, trimestre)


@router.get("/coralistas", response_model=list[DashboardCoralistaItemOut])
def coralistas_dashboard(
    ano: int | None = Query(default=None),
    trimestre: int | None = Query(default=None, ge=1, le=4),
    naipe: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[DashboardCoralistaItemOut]:
    return dashboard_coralistas(db, ano, trimestre, naipe)


@router.get("/naipes", response_model=list[DashboardNaipeItemOut])
def naipes_dashboard(
    ano: int | None = Query(default=None),
    trimestre: int | None = Query(default=None, ge=1, le=4),
    db: Session = Depends(get_db),
) -> list[DashboardNaipeItemOut]:
    return dashboard_naipes(db, ano, trimestre)

