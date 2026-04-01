from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, selectinload

from app.models.evento import Evento
from app.models.frequencia import Frequencia
from app.models.musica_evento import MusicaEvento
from app.models.trimestre import Trimestre
from app.schemas.evento import EventoCreate, EventoUpdate


def create_evento(db: Session, payload: EventoCreate) -> Evento:
    if not db.get(Trimestre, payload.trimestre_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trimestre não encontrado.")
    evento = Evento(**payload.model_dump())
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento


def get_evento_or_404(db: Session, evento_id: str) -> Evento:
    evento = (
        db.query(Evento)
        .options(
            selectinload(Evento.musicas).selectinload(MusicaEvento.escalas),
            selectinload(Evento.frequencias).selectinload(Frequencia.pessoa),
        )
        .where(Evento.id == evento_id)
        .first()
    )
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")
    return evento


def update_evento(db: Session, evento: Evento, payload: EventoUpdate) -> Evento:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(evento, key, value)
    db.commit()
    db.refresh(evento)
    return evento


def delete_evento(db: Session, evento: Evento) -> None:
    db.delete(evento)
    db.commit()
