from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, selectinload

from app.models.evento import Evento
from app.models.frequencia import Frequencia
from app.models.pessoa import Pessoa
from app.schemas.frequencia import FrequenciaBatchUpsertIn, FrequenciaPatchIn


def list_frequencias_by_evento(db: Session, evento_id: str) -> list[Frequencia]:
    if not db.get(Evento, evento_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")
    return (
        db.query(Frequencia)
        .options(selectinload(Frequencia.pessoa))
        .where(Frequencia.evento_id == evento_id)
        .order_by(Frequencia.pessoa_id.asc())
        .all()
    )


def get_frequencia_or_404(db: Session, frequencia_id: str) -> Frequencia:
    frequencia = db.get(Frequencia, frequencia_id)
    if not frequencia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Frequência não encontrada.")
    return frequencia


def upsert_frequencias_by_evento(db: Session, evento_id: str, payload: FrequenciaBatchUpsertIn) -> list[Frequencia]:
    if not db.get(Evento, evento_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")

    existing = {
        f.pessoa_id: f
        for f in db.query(Frequencia).where(Frequencia.evento_id == evento_id).all()
    }

    for item in payload.frequencias:
        if not db.get(Pessoa, item.pessoa_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pessoa '{item.pessoa_id}' não encontrada.")
        freq = existing.get(item.pessoa_id)
        if freq:
            freq.status = item.status
            freq.justificativa = item.justificativa
            freq.imagem_path = item.imagem_path
        else:
            db.add(
                Frequencia(
                    evento_id=evento_id,
                    pessoa_id=item.pessoa_id,
                    status=item.status,
                    justificativa=item.justificativa,
                    imagem_path=item.imagem_path,
                )
            )

    db.commit()
    return list_frequencias_by_evento(db, evento_id)


def patch_frequencia(db: Session, frequencia: Frequencia, payload: FrequenciaPatchIn) -> Frequencia:
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(frequencia, key, value)
    db.commit()
    db.refresh(frequencia)
    return frequencia

