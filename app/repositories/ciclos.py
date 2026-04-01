from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.ciclo import Ciclo
from app.models.trimestre import Trimestre
from app.schemas.ciclo import CicloCreate


def list_ciclos(db: Session) -> list[Ciclo]:
    return db.query(Ciclo).order_by(Ciclo.ano.desc()).all()


def get_ciclo_or_404(db: Session, ciclo_id: str) -> Ciclo:
    ciclo = db.get(Ciclo, ciclo_id)
    if not ciclo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ciclo não encontrado.")
    return ciclo


def create_ciclo(db: Session, payload: CicloCreate) -> Ciclo:
    ciclo = Ciclo(ano=payload.ano, ativo=payload.ativo)
    db.add(ciclo)
    try:
        db.flush()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ano de ciclo já cadastrado.") from exc

    if payload.criar_trimestres:
        for numero in range(1, 5):
            db.add(Trimestre(ciclo_id=ciclo.id, numero=numero))

    db.commit()
    db.refresh(ciclo)
    return ciclo

