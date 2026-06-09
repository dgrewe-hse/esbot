"""Initial ESBot schema.

Revision ID: 001
Revises:
Create Date: 2026-06-09

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create all ESBot tables."""
    op.create_table(
        "user_sessions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.String(length=128), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "last_activity_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_sessions_user_id"), "user_sessions", ["user_id"], unique=False)

    op.create_table(
        "messages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("session_id", sa.Uuid(), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["session_id"], ["user_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_messages_session_id"), "messages", ["session_id"], unique=False)

    op.create_table(
        "quiz_requests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("session_id", sa.Uuid(), nullable=False),
        sa.Column("topic", sa.String(length=256), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["session_id"], ["user_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_quiz_requests_session_id"), "quiz_requests", ["session_id"], unique=False
    )

    op.create_table(
        "quiz_items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("quiz_request_id", sa.Uuid(), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("options", sa.JSON(), nullable=False),
        sa.Column("correct_answer", sa.String(length=500), nullable=False),
        sa.ForeignKeyConstraint(["quiz_request_id"], ["quiz_requests.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_quiz_items_quiz_request_id"), "quiz_items", ["quiz_request_id"], unique=False
    )

    op.create_table(
        "submitted_answers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("quiz_item_id", sa.Uuid(), nullable=False),
        sa.Column("answer", sa.String(length=500), nullable=False),
        sa.Column(
            "submitted_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["quiz_item_id"], ["quiz_items.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_submitted_answers_quiz_item_id"),
        "submitted_answers",
        ["quiz_item_id"],
        unique=False,
    )

    op.create_table(
        "evaluation_results",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("submitted_answer_id", sa.Uuid(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("feedback", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["submitted_answer_id"], ["submitted_answers.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_evaluation_results_submitted_answer_id"),
        "evaluation_results",
        ["submitted_answer_id"],
        unique=True,
    )


def downgrade() -> None:
    """Drop all ESBot tables."""
    op.drop_index(
        op.f("ix_evaluation_results_submitted_answer_id"), table_name="evaluation_results"
    )
    op.drop_table("evaluation_results")
    op.drop_index(op.f("ix_submitted_answers_quiz_item_id"), table_name="submitted_answers")
    op.drop_table("submitted_answers")
    op.drop_index(op.f("ix_quiz_items_quiz_request_id"), table_name="quiz_items")
    op.drop_table("quiz_items")
    op.drop_index(op.f("ix_quiz_requests_session_id"), table_name="quiz_requests")
    op.drop_table("quiz_requests")
    op.drop_index(op.f("ix_messages_session_id"), table_name="messages")
    op.drop_table("messages")
    op.drop_index(op.f("ix_user_sessions_user_id"), table_name="user_sessions")
    op.drop_table("user_sessions")
