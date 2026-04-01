from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories import eventos as eventos_repo
from app.schemas.evento import EventoCreate, EventoOut, EventoUpdate
from app.services.files_service import delete_file_if_exists, save_event_attachment

router = APIRouter(tags=["eventos"])


@router.post("/eventos", response_model=EventoOut, status_code=201)
def criar_evento(payload: EventoCreate, db: Session = Depends(get_db)) -> EventoOut:
    return eventos_repo.create_evento(db, payload)


@router.get("/eventos/{evento_id}", response_model=EventoOut)
def obter_evento(evento_id: str, db: Session = Depends(get_db)) -> EventoOut:
    return eventos_repo.get_evento_or_404(db, evento_id)


@router.put("/eventos/{evento_id}", response_model=EventoOut)
def atualizar_evento(
    evento_id: str,
    payload: EventoUpdate,
    db: Session = Depends(get_db),
) -> EventoOut:
    evento = eventos_repo.get_evento_or_404(db, evento_id)
    return eventos_repo.update_evento(db, evento, payload)


@router.delete("/eventos/{evento_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def excluir_evento(evento_id: str, db: Session = Depends(get_db)) -> Response:
    evento = eventos_repo.get_evento_or_404(db, evento_id)
    delete_file_if_exists(evento.anexo_storage_path)
    eventos_repo.delete_evento(db, evento)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/eventos/{evento_id}/anexo", response_model=EventoOut)
def upload_anexo(
    evento_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> EventoOut:
    evento = eventos_repo.get_evento_or_404(db, evento_id)
    delete_file_if_exists(evento.anexo_storage_path)
    stored_path, original_name = save_event_attachment(evento.id, file)
    evento.anexo_storage_path = stored_path
    evento.anexo_nome = original_name
    evento.anexo_mime_type = file.content_type
    db.commit()
    db.refresh(evento)
    return evento


@router.get("/eventos/{evento_id}/anexo")
def baixar_anexo(evento_id: str, db: Session = Depends(get_db)) -> FileResponse:
    evento = eventos_repo.get_evento_or_404(db, evento_id)
    if not evento.anexo_storage_path:
        raise HTTPException(status_code=404, detail="Evento sem anexo.")
    path = Path(evento.anexo_storage_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Arquivo de anexo não encontrado no storage.")
    return FileResponse(
        path=path,
        media_type=evento.anexo_mime_type or "application/octet-stream",
        filename=evento.anexo_nome or path.name,
    )


@router.delete("/eventos/{evento_id}/anexo", response_model=EventoOut)
def remover_anexo(evento_id: str, db: Session = Depends(get_db)) -> EventoOut:
    evento = eventos_repo.get_evento_or_404(db, evento_id)
    delete_file_if_exists(evento.anexo_storage_path)
    evento.anexo_storage_path = None
    evento.anexo_nome = None
    evento.anexo_mime_type = None
    db.commit()
    db.refresh(evento)
    return evento

