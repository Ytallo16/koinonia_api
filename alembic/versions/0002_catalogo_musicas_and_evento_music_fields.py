"""catalogo de musicas e novos campos em musicas_evento

Revision ID: 0002_catalogo_musicas
Revises: 0001_initial_schema
Create Date: 2026-04-06 16:25:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0002_catalogo_musicas"
down_revision: Union[str, None] = "0001_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "catalogo_musicas",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("autor", sa.String(length=255), nullable=True),
        sa.Column("link", sa.String(length=500), nullable=True),
        sa.Column("descricao", sa.String(length=1000), nullable=False, server_default=""),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.add_column("musicas_evento", sa.Column("catalogo_musica_id", sa.String(length=36), nullable=True))
    op.add_column("musicas_evento", sa.Column("autor", sa.String(length=255), nullable=True))
    op.add_column("musicas_evento", sa.Column("descricao", sa.String(length=1000), nullable=False, server_default=""))
    op.create_foreign_key(
        "fk_musicas_evento_catalogo_musica",
        "musicas_evento",
        "catalogo_musicas",
        ["catalogo_musica_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_musicas_evento_catalogo_musica", "musicas_evento", type_="foreignkey")
    op.drop_column("musicas_evento", "descricao")
    op.drop_column("musicas_evento", "autor")
    op.drop_column("musicas_evento", "catalogo_musica_id")
    op.drop_table("catalogo_musicas")
