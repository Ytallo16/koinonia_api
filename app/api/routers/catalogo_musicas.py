from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories import catalogo_musicas as catalogo_repo
from app.schemas.catalogo_musica import CatalogoMusicaCreate, CatalogoMusicaOut, CatalogoMusicaUpdate

router = APIRouter(prefix="/catalogo-musicas", tags=["catalogo-musicas"])


@router.get("", response_model=list[CatalogoMusicaOut])
def listar_catalogo_musicas(
    apenas_ativas: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> list[CatalogoMusicaOut]:
    return catalogo_repo.list_catalogo_musicas(db, apenas_ativas=apenas_ativas)


@router.post("", response_model=CatalogoMusicaOut, status_code=status.HTTP_201_CREATED)
def criar_catalogo_musica(payload: CatalogoMusicaCreate, db: Session = Depends(get_db)) -> CatalogoMusicaOut:
    return catalogo_repo.create_catalogo_musica(db, payload)


@router.put("/{musica_id}", response_model=CatalogoMusicaOut)
def atualizar_catalogo_musica(
    musica_id: str,
    payload: CatalogoMusicaUpdate,
    db: Session = Depends(get_db),
) -> CatalogoMusicaOut:
    musica = catalogo_repo.get_catalogo_musica_or_404(db, musica_id)
    return catalogo_repo.update_catalogo_musica(db, musica, payload)


@router.delete("/{musica_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def excluir_catalogo_musica(musica_id: str, db: Session = Depends(get_db)) -> Response:
    musica = catalogo_repo.get_catalogo_musica_or_404(db, musica_id)
    catalogo_repo.delete_catalogo_musica(db, musica)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
