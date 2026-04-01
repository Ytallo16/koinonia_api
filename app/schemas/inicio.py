from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ProximoEventoOut(BaseModel):
    id: str
    nome: str
    data_hora: datetime
    trimestre_id: str


class InicioResumoOut(BaseModel):
    ano_ativo: int | None = None
    total_coralistas: int
    total_musicas: int
    total_eventos: int
    eventos_no_mes: int
    eventos_na_semana: int
    proximo_evento: ProximoEventoOut | None = None

