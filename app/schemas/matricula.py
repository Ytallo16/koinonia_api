from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from app.core.enums import FuncaoTrimestre
from app.schemas.pessoa import PessoaResumo


class MatriculaItemIn(BaseModel):
    pessoa_id: str
    funcao_no_trimestre: FuncaoTrimestre


class MatriculaBulkUpsertIn(BaseModel):
    matriculas: list[MatriculaItemIn]


class MatriculaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    trimestre_id: str
    pessoa_id: str
    funcao_no_trimestre: FuncaoTrimestre
    pessoa: PessoaResumo | None = None

