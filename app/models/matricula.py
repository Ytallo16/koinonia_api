from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import FuncaoTrimestre
from app.models.base import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.pessoa import Pessoa
    from app.models.trimestre import Trimestre


class Matricula(Base, UUIDMixin):
    __tablename__ = "matriculas"
    __table_args__ = (
        UniqueConstraint("trimestre_id", "pessoa_id", name="uq_matriculas_trimestre_pessoa"),
    )

    trimestre_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("trimestres.id", ondelete="CASCADE"),
        nullable=False,
    )
    pessoa_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("pessoas.id", ondelete="CASCADE"),
        nullable=False,
    )
    funcao_no_trimestre: Mapped[FuncaoTrimestre] = mapped_column(
        Enum(FuncaoTrimestre, name="funcao_trimestre_enum", native_enum=False),
        nullable=False,
    )

    trimestre: Mapped["Trimestre"] = relationship(back_populates="matriculas")
    pessoa: Mapped["Pessoa"] = relationship(back_populates="matriculas")

