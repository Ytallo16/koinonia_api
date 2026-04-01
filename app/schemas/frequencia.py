from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from app.core.enums import StatusFrequencia
from app.schemas.pessoa import PessoaResumo


class FrequenciaItemIn(BaseModel):
    pessoa_id: str
    status: StatusFrequencia
    justificativa: str | None = None
    imagem_path: str | None = None


class FrequenciaBatchUpsertIn(BaseModel):
    frequencias: list[FrequenciaItemIn]


class FrequenciaPatchIn(BaseModel):
    status: StatusFrequencia | None = None
    justificativa: str | None = None
    imagem_path: str | None = None


class FrequenciaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    evento_id: str
    pessoa_id: str
    status: StatusFrequencia
    justificativa: str | None = None
    imagem_path: str | None = None
    pessoa: PessoaResumo | None = None

