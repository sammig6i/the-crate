"""Initial migration

Revision ID: 001
Revises:
Create Date: 2024-03-19 10:00:00.000000

"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop existing tables and types
    op.execute("DROP TABLE IF EXISTS tracks")
    op.execute("DROP TABLE IF EXISTS albums")
    op.execute("DROP TYPE IF EXISTS albumstatus")

    op.create_enum(
        'albumstatus',
        ['pending', 'approved', 'rejected']
    )

    # Create albums table
    op.create_table(
        "albums",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("artist", sa.String(), nullable=False),
        sa.Column("release_date", sa.Date(), nullable=True),
        sa.Column("genre", sa.String(), nullable=True),
        sa.Column(
            "status",
            postgresql.ENUM('pending', 'approved', 'rejected', name='albumstatus'),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("storage_path", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Create tracks table
    op.create_table(
        "tracks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("album_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("track_number", sa.Integer(), nullable=False),
        sa.Column("duration", sa.Integer(), nullable=True),
        sa.Column("file_path", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["album_id"], ["albums.id"], ondelete="CASCADE"),
    )

    # Create indexes
    op.create_index(op.f("ix_albums_artist"), "albums", ["artist"])
    op.create_index(op.f("ix_albums_genre"), "albums", ["genre"])
    op.create_index(op.f("ix_albums_status"), "albums", ["status"])
    op.create_index(op.f("ix_tracks_album_id"), "tracks", ["album_id"])
    op.create_index(op.f("ix_tracks_track_number"), "tracks", ["track_number"])


def downgrade() -> None:
    # Drop tables first
    op.drop_table("tracks")
    op.drop_table("albums")

    # Drop enum type
    op.execute("DROP TYPE IF EXISTS albumstatus")
