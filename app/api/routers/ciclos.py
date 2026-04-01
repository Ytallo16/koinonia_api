from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories import ciclos as ciclos_repo
from app.repositories import trimestres as trimestres_repo
from app.schemas.ciclo import CicloCreate, CicloOut
from app.schemas.trimestre import TrimestreOut
from app.services.ciclos_service import ativar_ciclo_exclusivo

router = APIRouter(prefix="/ciclos", tags=["ciclos"])


@router.get("", response_model=list[CicloOut])
def listar_ciclos(db: Session = Depends(get_db)) -> list[CicloOut]:
    return ciclos_repo.list_ciclos(db)


@router.post("", response_model=CicloOut, status_code=201)
def criar_ciclo(payload: CicloCreate, db: Session = Depends(get_db)) -> CicloOut:
    ciclo = ciclos_repo.create_ciclo(db, payload)
    if payload.ativo:
        ciclo = ativar_ciclo_exclusivo(db, ciclo)
    return ciclo


@router.patch("/{ciclo_id}/ativar", response_model=CicloOut)
def ativar_ciclo(ciclo_id: str, db: Session = Depends(get_db)) -> CicloOut:
    ciclo = ciclos_repo.get_ciclo_or_404(db, ciclo_id)
    return ativar_ciclo_exclusivo(db, ciclo)


@router.get("/{ciclo_id}/trimestres", response_model=list[TrimestreOut])
def listar_trimestres_por_ciclo(ciclo_id: str, db: Session = Depends(get_db)) -> list[TrimestreOut]:
    ciclos_repo.get_ciclo_or_404(db, ciclo_id)
    return trimestres_repo.list_trimestres_by_ciclo(db, ciclo_id)

