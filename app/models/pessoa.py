from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import ClassificacaoVocal, TipoPessoa
from app.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.frequencia import Frequencia
    from app.models.matricula import Matricula
    from app.models.musica_escala import MusicaEscala


class Pessoa(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "pessoas"

    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    data_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
    telefone: Mapped[str] = mapped_column(String(30), nullable=False)
    classificacao_vocal: Mapped[ClassificacaoVocal] = mapped_column(
        Enum(ClassificacaoVocal, name="classificacao_vocal_enum", native_enum=False),
        nullable=False,
    )
    tipo_padrao: Mapped[TipoPessoa] = mapped_column(
        Enum(TipoPessoa, name="tipo_pessoa_enum", native_enum=False),
        nullable=False,
    )
    foto_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    matriculas: Mapped[list["Matricula"]] = relationship(
        back_populates="pessoa",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    frequencias: Mapped[list["Frequencia"]] = relationship(
        back_populates="pessoa",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    escalas: Mapped[list["MusicaEscala"]] = relationship(
        back_populates="pessoa",
        passive_deletes=True,
    )

