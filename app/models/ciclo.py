from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.trimestre import Trimestre


class Ciclo(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "ciclos"
    __table_args__ = (UniqueConstraint("ano", name="uq_ciclos_ano"),)

    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    trimestres: Mapped[list["Trimestre"]] = relationship(
        back_populates="ciclo",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

