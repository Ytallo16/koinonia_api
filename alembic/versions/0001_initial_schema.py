"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-04-01 11:20:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


classificacao_vocal_enum = sa.Enum(
    "soprano",
    "contralto",
    "tenor",
    "baixo",
    "na",
    name="classificacao_vocal_enum",
    native_enum=False,
)
tipo_pessoa_enum = sa.Enum(
    "coralista",
    "membro",
    "regente",
    name="tipo_pessoa_enum",
    native_enum=False,
)
funcao_trimestre_enum = sa.Enum(
    "coralista",
    "membro",
    "regente",
    name="funcao_trimestre_enum",
    native_enum=False,
)
status_frequencia_enum = sa.Enum(
    "presenca",
    "falta",
    "atraso",
    "falta_justificada",
    name="status_frequencia_enum",
    native_enum=False,
)
naipe_enum = sa.Enum(
    "soprano",
    "contralto",
    "tenor",
    "baixo",
    name="naipe_enum",
    native_enum=False,
)


def upgrade() -> None:
    op.create_table(
        "pessoas",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("data_nascimento", sa.Date(), nullable=False),
        sa.Column("telefone", sa.String(length=30), nullable=False),
        sa.Column("classificacao_vocal", classificacao_vocal_enum, nullable=False),
        sa.Column("tipo_padrao", tipo_pessoa_enum, nullable=False),
        sa.Column("foto_url", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "ciclos",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ano", name="uq_ciclos_ano"),
    )

    op.create_table(
        "trimestres",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("ciclo_id", sa.String(length=36), nullable=False),
        sa.Column("numero", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["ciclo_id"], ["ciclos.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ciclo_id", "numero", name="uq_trimestres_ciclo_numero"),
    )

    op.create_table(
        "matriculas",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("trimestre_id", sa.String(length=36), nullable=False),
        sa.Column("pessoa_id", sa.String(length=36), nullable=False),
        sa.Column("funcao_no_trimestre", funcao_trimestre_enum, nullable=False),
        sa.ForeignKeyConstraint(["trimestre_id"], ["trimestres.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["pessoa_id"], ["pessoas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("trimestre_id", "pessoa_id", name="uq_matriculas_trimestre_pessoa"),
    )

    op.create_table(
        "eventos",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("trimestre_id", sa.String(length=36), nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("descricao", sa.String(length=1000), nullable=False),
        sa.Column("data_hora", sa.DateTime(timezone=True), nullable=False),
        sa.Column("tipo", sa.String(length=100), nullable=True),
        sa.Column("anexo_nome", sa.String(length=255), nullable=True),
        sa.Column("anexo_mime_type", sa.String(length=100), nullable=True),
        sa.Column("anexo_storage_path", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["trimestre_id"], ["trimestres.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "musicas_evento",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("evento_id", sa.String(length=36), nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("link", sa.String(length=500), nullable=True),
        sa.Column("ordem", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.ForeignKeyConstraint(["evento_id"], ["eventos.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "frequencias",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("evento_id", sa.String(length=36), nullable=False),
        sa.Column("pessoa_id", sa.String(length=36), nullable=False),
        sa.Column("status", status_frequencia_enum, nullable=False),
        sa.Column("justificativa", sa.String(length=1000), nullable=True),
        sa.Column("imagem_path", sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(["evento_id"], ["eventos.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["pessoa_id"], ["pessoas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("evento_id", "pessoa_id", name="uq_frequencias_evento_pessoa"),
    )

    op.create_table(
        "musica_escalas",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("musica_id", sa.String(length=36), nullable=False),
        sa.Column("naipe", naipe_enum, nullable=False),
        sa.Column("pessoa_id", sa.String(length=36), nullable=True),
        sa.ForeignKeyConstraint(["musica_id"], ["musicas_evento.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["pessoa_id"], ["pessoas.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("musica_id", "naipe", name="uq_musica_escalas_musica_naipe"),
    )


def downgrade() -> None:
    op.drop_table("musica_escalas")
    op.drop_table("frequencias")
    op.drop_table("musicas_evento")
    op.drop_table("eventos")
    op.drop_table("matriculas")
    op.drop_table("trimestres")
    op.drop_table("ciclos")
    op.drop_table("pessoas")
