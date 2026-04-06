from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, selectinload

from app.models.evento import Evento
from app.models.catalogo_musica import CatalogoMusica
from app.models.musica_escala import MusicaEscala
from app.models.musica_evento import MusicaEvento
from app.models.pessoa import Pessoa
from app.schemas.musica import EscalasBulkIn, MusicaCreate, MusicasSelecaoIn, MusicaUpdate


def list_musicas_by_evento(db: Session, evento_id: str) -> list[MusicaEvento]:
    if not db.get(Evento, evento_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")
    return (
        db.query(MusicaEvento)
        .options(selectinload(MusicaEvento.escalas).selectinload(MusicaEscala.pessoa))
        .where(MusicaEvento.evento_id == evento_id)
        .order_by(MusicaEvento.ordem.asc(), MusicaEvento.nome.asc())
        .all()
    )


def get_musica_or_404(db: Session, musica_id: str) -> MusicaEvento:
    musica = (
        db.query(MusicaEvento)
        .options(selectinload(MusicaEvento.escalas).selectinload(MusicaEscala.pessoa))
        .where(MusicaEvento.id == musica_id)
        .first()
    )
    if not musica:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Música não encontrada.")
    return musica


def create_musica(db: Session, evento_id: str, payload: MusicaCreate) -> MusicaEvento:
    if not db.get(Evento, evento_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")

    catalogo: CatalogoMusica | None = None
    if payload.catalogo_musica_id:
        catalogo = db.get(CatalogoMusica, payload.catalogo_musica_id)
        if not catalogo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Música de catálogo '{payload.catalogo_musica_id}' não encontrada.",
            )

    musica = MusicaEvento(
        evento_id=evento_id,
        catalogo_musica_id=catalogo.id if catalogo else payload.catalogo_musica_id,
        nome=payload.nome,
        autor=payload.autor,
        link=payload.link,
        descricao=payload.descricao,
        ordem=payload.ordem,
    )
    db.add(musica)
    db.flush()

    for escala in payload.escalas:
        if escala.pessoa_id and not db.get(Pessoa, escala.pessoa_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pessoa '{escala.pessoa_id}' não encontrada.")
        db.add(MusicaEscala(musica_id=musica.id, naipe=escala.naipe, pessoa_id=escala.pessoa_id))

    db.commit()
    db.refresh(musica)
    return get_musica_or_404(db, musica.id)


def add_catalogo_musicas_to_evento(
    db: Session,
    evento_id: str,
    payload: MusicasSelecaoIn,
) -> list[MusicaEvento]:
    if not db.get(Evento, evento_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")

    ids = [item for item in payload.catalogo_musica_ids if item]
    if not ids:
        return list_musicas_by_evento(db, evento_id)

    existentes = (
        db.query(MusicaEvento)
        .where(MusicaEvento.evento_id == evento_id, MusicaEvento.catalogo_musica_id.in_(ids))
        .all()
    )
    ids_existentes = {musica.catalogo_musica_id for musica in existentes if musica.catalogo_musica_id}

    ultima_ordem = (
        db.query(MusicaEvento.ordem)
        .where(MusicaEvento.evento_id == evento_id)
        .order_by(MusicaEvento.ordem.desc())
        .limit(1)
        .scalar()
    )
    ordem_atual = (ultima_ordem or -1) + 1

    for catalogo_id in ids:
        if catalogo_id in ids_existentes:
            continue
        catalogo = db.get(CatalogoMusica, catalogo_id)
        if not catalogo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Música de catálogo '{catalogo_id}' não encontrada.",
            )
        db.add(
            MusicaEvento(
                evento_id=evento_id,
                catalogo_musica_id=catalogo.id,
                nome=catalogo.nome,
                autor=catalogo.autor,
                link=catalogo.link,
                descricao=catalogo.descricao or "",
                ordem=ordem_atual,
            )
        )
        ordem_atual += 1

    db.commit()
    return list_musicas_by_evento(db, evento_id)


def update_musica(db: Session, musica: MusicaEvento, payload: MusicaUpdate) -> MusicaEvento:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(musica, key, value)
    db.commit()
    db.refresh(musica)
    return get_musica_or_404(db, musica.id)


def delete_musica(db: Session, musica: MusicaEvento) -> None:
    db.delete(musica)
    db.commit()


def replace_escalas(db: Session, musica: MusicaEvento, payload: EscalasBulkIn) -> MusicaEvento:
    by_naipe = {}
    for item in payload.escalas:
        by_naipe[item.naipe] = item.pessoa_id
    for pessoa_id in [p for p in by_naipe.values() if p]:
        if not db.get(Pessoa, pessoa_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pessoa '{pessoa_id}' não encontrada.")

    existing = {e.naipe: e for e in musica.escalas}
    for naipe, pessoa_id in by_naipe.items():
        if naipe in existing:
            existing[naipe].pessoa_id = pessoa_id
        else:
            db.add(MusicaEscala(musica_id=musica.id, naipe=naipe, pessoa_id=pessoa_id))

    for naipe, escala in existing.items():
        if naipe not in by_naipe:
            db.delete(escala)

    db.commit()
    return get_musica_or_404(db, musica.id)
