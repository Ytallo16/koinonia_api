from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.pessoa import Pessoa
from app.schemas.pessoa import PessoaCreate, PessoaUpdate


def list_pessoas(db: Session) -> list[Pessoa]:
    return db.query(Pessoa).order_by(Pessoa.nome.asc()).all()


def get_pessoa_or_404(db: Session, pessoa_id: str) -> Pessoa:
    pessoa = db.get(Pessoa, pessoa_id)
    if not pessoa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pessoa não encontrada.")
    return pessoa


def create_pessoa(db: Session, payload: PessoaCreate) -> Pessoa:
    pessoa = Pessoa(**payload.model_dump())
    db.add(pessoa)
    db.commit()
    db.refresh(pessoa)
    return pessoa


def update_pessoa(db: Session, pessoa: Pessoa, payload: PessoaUpdate) -> Pessoa:
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(pessoa, key, value)
    db.commit()
    db.refresh(pessoa)
    return pessoa


def delete_pessoa(db: Session, pessoa: Pessoa) -> None:
    db.delete(pessoa)
    db.commit()

