from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories import pessoas as pessoas_repo
from app.schemas.pessoa import PessoaCreate, PessoaOut, PessoaUpdate

router = APIRouter(prefix="/pessoas", tags=["pessoas"])


@router.get("", response_model=list[PessoaOut])
def listar_pessoas(db: Session = Depends(get_db)) -> list[PessoaOut]:
    return pessoas_repo.list_pessoas(db)


@router.post("", response_model=PessoaOut, status_code=status.HTTP_201_CREATED)
def criar_pessoa(payload: PessoaCreate, db: Session = Depends(get_db)) -> PessoaOut:
    return pessoas_repo.create_pessoa(db, payload)


@router.put("/{pessoa_id}", response_model=PessoaOut)
def atualizar_pessoa(
    pessoa_id: str,
    payload: PessoaUpdate,
    db: Session = Depends(get_db),
) -> PessoaOut:
    pessoa = pessoas_repo.get_pessoa_or_404(db, pessoa_id)
    return pessoas_repo.update_pessoa(db, pessoa, payload)


@router.delete("/{pessoa_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def excluir_pessoa(pessoa_id: str, db: Session = Depends(get_db)) -> Response:
    pessoa = pessoas_repo.get_pessoa_or_404(db, pessoa_id)
    pessoas_repo.delete_pessoa(db, pessoa)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

