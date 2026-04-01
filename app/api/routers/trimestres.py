from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories import matriculas as matriculas_repo
from app.repositories import trimestres as trimestres_repo
from app.schemas.evento import EventoOut
from app.schemas.matricula import MatriculaBulkUpsertIn, MatriculaOut
from app.schemas.trimestre import TrimestreCreate, TrimestreOut
from app.services.eventos_service import sort_eventos_like_app

router = APIRouter(tags=["trimestres"])


@router.post("/trimestres", response_model=TrimestreOut, status_code=201)
def criar_trimestre(payload: TrimestreCreate, db: Session = Depends(get_db)) -> TrimestreOut:
    return trimestres_repo.create_trimestre(db, payload)


@router.get("/trimestres/{trimestre_id}/matriculas", response_model=list[MatriculaOut])
def listar_matriculas(trimestre_id: str, db: Session = Depends(get_db)) -> list[MatriculaOut]:
    return matriculas_repo.list_matriculas_by_trimestre(db, trimestre_id)


@router.put("/trimestres/{trimestre_id}/matriculas", response_model=list[MatriculaOut])
def upsert_matriculas(
    trimestre_id: str,
    payload: MatriculaBulkUpsertIn,
    db: Session = Depends(get_db),
) -> list[MatriculaOut]:
    return matriculas_repo.upsert_matriculas_by_trimestre(db, trimestre_id, payload)


@router.get("/trimestres/{trimestre_id}/eventos", response_model=list[EventoOut])
def listar_eventos_trimestre(trimestre_id: str, db: Session = Depends(get_db)) -> list[EventoOut]:
    trimestres_repo.get_trimestre_or_404(db, trimestre_id)
    eventos = trimestres_repo.list_eventos_by_trimestre(db, trimestre_id)
    return sort_eventos_like_app(eventos)

