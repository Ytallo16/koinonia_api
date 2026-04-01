from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CicloCreate(BaseModel):
    ano: int
    ativo: bool = False
    criar_trimestres: bool = True


class CicloOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    ano: int
    ativo: bool
    created_at: datetime
    updated_at: datetime

