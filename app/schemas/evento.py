from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventoCreate(BaseModel):
    trimestre_id: str
    nome: str
    descricao: str = ""
    data_hora: datetime
    tipo: str | None = None


class EventoUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    data_hora: datetime | None = None
    tipo: str | None = None


class EventoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    trimestre_id: str
    nome: str
    descricao: str
    data_hora: datetime
    tipo: str | None = None
    anexo_nome: str | None = None
    anexo_mime_type: str | None = None
    anexo_storage_path: str | None = None
    created_at: datetime
    updated_at: datetime

