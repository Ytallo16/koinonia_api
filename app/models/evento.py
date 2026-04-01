from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.frequencia import Frequencia
    from app.models.musica_evento import MusicaEvento
    from app.models.trimestre import Trimestre


class Evento(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "eventos"

    trimestre_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("trimestres.id", ondelete="CASCADE"),
        nullable=False,
    )
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao: Mapped[str] = mapped_column(String(1000), nullable=False, default="")
    data_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    tipo: Mapped[str | None] = mapped_column(String(100), nullable=True)

    anexo_nome: Mapped[str | None] = mapped_column(String(255), nullable=True)
    anexo_mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    anexo_storage_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    trimestre: Mapped["Trimestre"] = relationship(back_populates="eventos")
    frequencias: Mapped[list["Frequencia"]] = relationship(
        back_populates="evento",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    musicas: Mapped[list["MusicaEvento"]] = relationship(
        back_populates="evento",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

