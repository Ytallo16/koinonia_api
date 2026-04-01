from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TrimestreCreate(BaseModel):
    ciclo_id: str
    numero: int = Field(ge=1, le=4)


class TrimestreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    ciclo_id: str
    numero: int

