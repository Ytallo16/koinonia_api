from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import Naipe
from app.schemas.pessoa import PessoaResumo


class EscalaIn(BaseModel):
    naipe: Naipe
    pessoa_id: str | None = None


class EscalaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    musica_id: str
    naipe: Naipe
    pessoa_id: str | None = None
    pessoa: PessoaResumo | None = None


class MusicaCreate(BaseModel):
    catalogo_musica_id: str | None = None
    nome: str
    autor: str | None = None
    link: str | None = None
    descricao: str = ""
    ordem: int = Field(default=0, ge=0)
    escalas: list[EscalaIn] = Field(default_factory=list)


class MusicaUpdate(BaseModel):
    nome: str | None = None
    autor: str | None = None
    link: str | None = None
    descricao: str | None = None
    ordem: int | None = Field(default=None, ge=0)


class EscalasBulkIn(BaseModel):
    escalas: list[EscalaIn]


class MusicaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    evento_id: str
    catalogo_musica_id: str | None = None
    nome: str
    autor: str | None = None
    link: str | None = None
    descricao: str
    ordem: int
    escalas: list[EscalaOut] = Field(default_factory=list)


class MusicasSelecaoIn(BaseModel):
    catalogo_musica_ids: list[str]
