from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.inicio import InicioResumoOut
from app.services.inicio_service import inicio_resumo

router = APIRouter(prefix="/inicio", tags=["inicio"])


@router.get("/resumo", response_model=InicioResumoOut)
def resumo_inicio(db: Session = Depends(get_db)) -> InicioResumoOut:
    return inicio_resumo(db)

