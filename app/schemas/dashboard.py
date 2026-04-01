from __future__ import annotations

from pydantic import BaseModel


class DashboardResumoOut(BaseModel):
    coralistas: int
    eventos: int
    presencas: int
    faltas: int
    faltas_justificadas: int
    percentual_presenca: float
    percentual_falta: float
    percentual_falta_justificada: float


class DashboardCoralistaItemOut(BaseModel):
    pessoa_id: str
    nome: str
    classificacao_vocal: str
    presencas: int
    faltas: int
    faltas_justificadas: int
    total: int
    percentual_presenca: int


class DashboardNaipeItemOut(BaseModel):
    naipe: str
    membros: int
    presencas: int
    faltas: int
    faltas_justificadas: int
    total: int
    percentual_presenca: int
    membros_detalhe: list[DashboardCoralistaItemOut]

