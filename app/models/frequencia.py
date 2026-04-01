from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import StatusFrequencia
from app.models.base import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.evento import Evento
    from app.models.pessoa import Pessoa


class Frequencia(Base, UUIDMixin):
    __tablename__ = "frequencias"
    __table_args__ = (
        UniqueConstraint("evento_id", "pessoa_id", name="uq_frequencias_evento_pessoa"),
    )

    evento_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("eventos.id", ondelete="CASCADE"),
        nullable=False,
    )
    pessoa_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("pessoas.id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[StatusFrequencia] = mapped_column(
        Enum(StatusFrequencia, name="status_frequencia_enum", native_enum=False),
        nullable=False,
    )
    justificativa: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    imagem_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    evento: Mapped["Evento"] = relationship(back_populates="frequencias")
    pessoa: Mapped["Pessoa"] = relationship(back_populates="frequencias")

