from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.catalogo_musica import CatalogoMusica
    from app.models.evento import Evento
    from app.models.musica_escala import MusicaEscala


class MusicaEvento(Base, UUIDMixin):
    __tablename__ = "musicas_evento"

    evento_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("eventos.id", ondelete="CASCADE"),
        nullable=False,
    )
    catalogo_musica_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("catalogo_musicas.id", ondelete="SET NULL"),
        nullable=True,
    )
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    autor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    descricao: Mapped[str] = mapped_column(String(1000), nullable=False, default="")
    ordem: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    evento: Mapped["Evento"] = relationship(back_populates="musicas")
    catalogo_musica: Mapped["CatalogoMusica | None"] = relationship(back_populates="musicas_evento")
    escalas: Mapped[list["MusicaEscala"]] = relationship(
        back_populates="musica",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
