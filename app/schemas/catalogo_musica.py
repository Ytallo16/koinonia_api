from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CatalogoMusicaBase(BaseModel):
    nome: str
    autor: str | None = None
    link: str | None = None
    descricao: str = ""
    ativo: bool = True


class CatalogoMusicaCreate(CatalogoMusicaBase):
    pass


class CatalogoMusicaUpdate(BaseModel):
    nome: str | None = None
    autor: str | None = None
    link: str | None = None
    descricao: str | None = None
    ativo: bool | None = None


class CatalogoMusicaOut(CatalogoMusicaBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
