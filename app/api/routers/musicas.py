from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories import musicas as musicas_repo
from app.schemas.musica import EscalasBulkIn, MusicaCreate, MusicaOut, MusicaUpdate

router = APIRouter(tags=["musicas"])


@router.get("/eventos/{evento_id}/musicas", response_model=list[MusicaOut])
def listar_musicas_evento(evento_id: str, db: Session = Depends(get_db)) -> list[MusicaOut]:
    return musicas_repo.list_musicas_by_evento(db, evento_id)


@router.post("/eventos/{evento_id}/musicas", response_model=MusicaOut, status_code=201)
def criar_musica_evento(
    evento_id: str,
    payload: MusicaCreate,
    db: Session = Depends(get_db),
) -> MusicaOut:
    return musicas_repo.create_musica(db, evento_id, payload)


@router.put("/eventos/{evento_id}/musicas/{musica_id}", response_model=MusicaOut)
def atualizar_musica_evento(
    evento_id: str,
    musica_id: str,
    payload: MusicaUpdate,
    db: Session = Depends(get_db),
) -> MusicaOut:
    musica = musicas_repo.get_musica_or_404(db, musica_id)
    if musica.evento_id != evento_id:
        raise HTTPException(status_code=404, detail="Música não pertence ao evento informado.")
    return musicas_repo.update_musica(db, musica, payload)


@router.delete("/eventos/{evento_id}/musicas/{musica_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def excluir_musica_evento(evento_id: str, musica_id: str, db: Session = Depends(get_db)) -> Response:
    musica = musicas_repo.get_musica_or_404(db, musica_id)
    if musica.evento_id != evento_id:
        raise HTTPException(status_code=404, detail="Música não pertence ao evento informado.")
    musicas_repo.delete_musica(db, musica)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/musicas/{musica_id}/escalas", response_model=MusicaOut)
def substituir_escalas_musica(
    musica_id: str,
    payload: EscalasBulkIn,
    db: Session = Depends(get_db),
) -> MusicaOut:
    musica = musicas_repo.get_musica_or_404(db, musica_id)
    return musicas_repo.replace_escalas(db, musica, payload)
