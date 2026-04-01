from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.matricula import Matricula
from app.models.pessoa import Pessoa
from app.models.trimestre import Trimestre
from app.schemas.matricula import MatriculaBulkUpsertIn


def list_matriculas_by_trimestre(db: Session, trimestre_id: str) -> list[Matricula]:
    if not db.get(Trimestre, trimestre_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trimestre não encontrado.")
    return (
        db.query(Matricula)
        .options(joinedload(Matricula.pessoa))
        .where(Matricula.trimestre_id == trimestre_id)
        .order_by(Matricula.pessoa_id.asc())
        .all()
    )


def upsert_matriculas_by_trimestre(db: Session, trimestre_id: str, payload: MatriculaBulkUpsertIn) -> list[Matricula]:
    if not db.get(Trimestre, trimestre_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trimestre não encontrado.")

    incoming = {item.pessoa_id: item.funcao_no_trimestre for item in payload.matriculas}
    for pessoa_id in incoming.keys():
        if not db.get(Pessoa, pessoa_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pessoa '{pessoa_id}' não encontrada.")

    existing = {
        item.pessoa_id: item
        for item in db.query(Matricula).where(Matricula.trimestre_id == trimestre_id).all()
    }

    for pessoa_id, funcao in incoming.items():
        if pessoa_id in existing:
            existing[pessoa_id].funcao_no_trimestre = funcao
        else:
            db.add(Matricula(trimestre_id=trimestre_id, pessoa_id=pessoa_id, funcao_no_trimestre=funcao))

    for pessoa_id, item in existing.items():
        if pessoa_id not in incoming:
            db.delete(item)

    db.commit()
    return list_matriculas_by_trimestre(db, trimestre_id)

