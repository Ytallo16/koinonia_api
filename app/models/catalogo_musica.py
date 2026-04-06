from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.musica_evento import MusicaEvento


class CatalogoMusica(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "catalogo_musicas"

    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    autor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    descricao: Mapped[str] = mapped_column(String(1000), nullable=False, default="")
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))

    musicas_evento: Mapped[list["MusicaEvento"]] = relationship(back_populates="catalogo_musica")
