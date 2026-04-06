from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.catalogo_musica import CatalogoMusica
from app.schemas.catalogo_musica import CatalogoMusicaCreate, CatalogoMusicaUpdate


def list_catalogo_musicas(db: Session, apenas_ativas: bool = False) -> list[CatalogoMusica]:
    query = db.query(CatalogoMusica)
    if apenas_ativas:
        query = query.where(CatalogoMusica.ativo.is_(True))
    return query.order_by(CatalogoMusica.nome.asc()).all()


def get_catalogo_musica_or_404(db: Session, musica_id: str) -> CatalogoMusica:
    musica = db.get(CatalogoMusica, musica_id)
    if not musica:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Música de catálogo não encontrada.")
    return musica


def create_catalogo_musica(db: Session, payload: CatalogoMusicaCreate) -> CatalogoMusica:
    musica = CatalogoMusica(**payload.model_dump())
    db.add(musica)
    db.commit()
    db.refresh(musica)
    return musica


def update_catalogo_musica(db: Session, musica: CatalogoMusica, payload: CatalogoMusicaUpdate) -> CatalogoMusica:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(musica, key, value)
    db.commit()
    db.refresh(musica)
    return musica


def delete_catalogo_musica(db: Session, musica: CatalogoMusica) -> None:
    db.delete(musica)
    db.commit()
