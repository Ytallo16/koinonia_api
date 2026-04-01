from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import Naipe
from app.models.base import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.musica_evento import MusicaEvento
    from app.models.pessoa import Pessoa


class MusicaEscala(Base, UUIDMixin):
    __tablename__ = "musica_escalas"
    __table_args__ = (
        UniqueConstraint("musica_id", "naipe", name="uq_musica_escalas_musica_naipe"),
    )

    musica_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("musicas_evento.id", ondelete="CASCADE"),
        nullable=False,
    )
    naipe: Mapped[Naipe] = mapped_column(
        Enum(Naipe, name="naipe_enum", native_enum=False),
        nullable=False,
    )
    pessoa_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("pessoas.id", ondelete="SET NULL"),
        nullable=True,
    )

    musica: Mapped["MusicaEvento"] = relationship(back_populates="escalas")
    pessoa: Mapped["Pessoa | None"] = relationship(back_populates="escalas")
