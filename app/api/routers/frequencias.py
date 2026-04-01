from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories import frequencias as frequencias_repo
from app.schemas.frequencia import FrequenciaBatchUpsertIn, FrequenciaOut, FrequenciaPatchIn

router = APIRouter(tags=["frequencias"])


@router.get("/eventos/{evento_id}/frequencias", response_model=list[FrequenciaOut])
def listar_frequencias_evento(evento_id: str, db: Session = Depends(get_db)) -> list[FrequenciaOut]:
    return frequencias_repo.list_frequencias_by_evento(db, evento_id)


@router.put("/eventos/{evento_id}/frequencias", response_model=list[FrequenciaOut])
def upsert_frequencias_evento(
    evento_id: str,
    payload: FrequenciaBatchUpsertIn,
    db: Session = Depends(get_db),
) -> list[FrequenciaOut]:
    return frequencias_repo.upsert_frequencias_by_evento(db, evento_id, payload)


@router.patch("/frequencias/{frequencia_id}", response_model=FrequenciaOut)
def atualizar_frequencia(
    frequencia_id: str,
    payload: FrequenciaPatchIn,
    db: Session = Depends(get_db),
) -> FrequenciaOut:
    freq = frequencias_repo.get_frequencia_or_404(db, frequencia_id)
    return frequencias_repo.patch_frequencia(db, freq, payload)

