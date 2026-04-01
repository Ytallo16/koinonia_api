from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.ciclo import Ciclo
    from app.models.evento import Evento
    from app.models.matricula import Matricula


class Trimestre(Base, UUIDMixin):
    __tablename__ = "trimestres"
    __table_args__ = (
        UniqueConstraint("ciclo_id", "numero", name="uq_trimestres_ciclo_numero"),
    )

    ciclo_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("ciclos.id", ondelete="CASCADE"),
        nullable=False,
    )
    numero: Mapped[int] = mapped_column(Integer, nullable=False)

    ciclo: Mapped["Ciclo"] = relationship(back_populates="trimestres")
    matriculas: Mapped[list["Matricula"]] = relationship(
        back_populates="trimestre",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    eventos: Mapped[list["Evento"]] = relationship(
        back_populates="trimestre",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

