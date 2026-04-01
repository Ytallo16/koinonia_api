from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import ClassificacaoVocal, TipoPessoa


class PessoaBase(BaseModel):
    nome: str
    data_nascimento: date
    telefone: str
    classificacao_vocal: ClassificacaoVocal
    tipo_padrao: TipoPessoa
    foto_url: str | None = None


class PessoaCreate(PessoaBase):
    pass


class PessoaUpdate(BaseModel):
    nome: str | None = None
    data_nascimento: date | None = None
    telefone: str | None = None
    classificacao_vocal: ClassificacaoVocal | None = None
    tipo_padrao: TipoPessoa | None = None
    foto_url: str | None = None


class PessoaOut(PessoaBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime


class PessoaResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nome: str
    classificacao_vocal: ClassificacaoVocal
    tipo_padrao: TipoPessoa

