from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.ciclo import Ciclo


def ativar_ciclo_exclusivo(db: Session, ciclo: Ciclo) -> Ciclo:
    db.query(Ciclo).update({Ciclo.ativo: False})
    ciclo.ativo = True
    db.commit()
    db.refresh(ciclo)
    return ciclo

