from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models.ciclo import Ciclo
from app.models.evento import Evento
from app.models.trimestre import Trimestre
from app.schemas.trimestre import TrimestreCreate


def get_trimestre_or_404(db: Session, trimestre_id: str) -> Trimestre:
    trimestre = db.get(Trimestre, trimestre_id)
    if not trimestre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trimestre não encontrado.")
    return trimestre


def list_trimestres_by_ciclo(db: Session, ciclo_id: str) -> list[Trimestre]:
    return (
        db.query(Trimestre)
        .where(Trimestre.ciclo_id == ciclo_id)
        .order_by(Trimestre.numero.asc())
        .all()
    )


def create_trimestre(db: Session, payload: TrimestreCreate) -> Trimestre:
    if not db.get(Ciclo, payload.ciclo_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ciclo não encontrado.")
    trimestre = Trimestre(ciclo_id=payload.ciclo_id, numero=payload.numero)
    db.add(trimestre)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Trimestre já existe para esse ciclo.",
        ) from exc
    db.refresh(trimestre)
    return trimestre


def list_eventos_by_trimestre(db: Session, trimestre_id: str) -> list[Evento]:
    return (
        db.query(Evento)
        .where(Evento.trimestre_id == trimestre_id)
        .options(selectinload(Evento.musicas))
        .all()
    )

