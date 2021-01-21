"""empty message

Revision ID: 8aa8f8d6a0c3
Revises:
Create Date: 2017-04-24 10:24:46.888136

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from sqlalchemy import Integer


# revision identifiers, used by Alembic.
revision = "8aa8f8d6a0c3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "areas_of_interest",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(geometry_type="MULTIPOLYGON", srid=4326),
            nullable=True,
        ),
        sa.Column(
            "centroid",
            geoalchemy2.types.Geometry(geometry_type="POINT", srid=4326),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organisations", sa.String(), nullable=True),
        sa.Column("campaigns", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("campaigns"),
        sa.UniqueConstraint("organisations"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("role", sa.Integer(), nullable=False),
        sa.Column("mapping_level", sa.Integer(), nullable=False),
        sa.Column("tasks_mapped", sa.Integer(), nullable=False),
        sa.Column("tasks_validated", sa.Integer(), nullable=False),
        sa.Column("tasks_invalidated", sa.Integer(), nullable=False),
        sa.Column("projects_mapped", sa.ARRAY(Integer()), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("status", sa.Integer(), nullable=False),
        sa.Column("aoi_id", sa.Integer(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=True),
        sa.Column("default_locale", sa.String(length=10), nullable=True),
        sa.Column("author_id", sa.BigInteger(), nullable=False),
        sa.Column("mapper_level", sa.Integer(), nullable=False),
        sa.Column("enforce_mapper_level", sa.Boolean(), nullable=True),
        sa.Column("enforce_validator_role", sa.Boolean(), nullable=True),
        sa.Column("private", sa.Boolean(), nullable=True),
        sa.Column("entities_to_map", sa.String(), nullable=True),
        sa.Column("changeset_comment", sa.String(), nullable=True),
        sa.Column("due_date", sa.DateTime(), nullable=True),
        sa.Column("imagery", sa.String(), nullable=True),
        sa.Column("josm_preset", sa.String(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("mapping_types", sa.ARRAY(Integer()), nullable=True),
        sa.Column("organisation_tag", sa.String(), nullable=True),
        sa.Column("campaign_tag", sa.String(), nullable=True),
        sa.Column("total_tasks", sa.Integer(), nullable=False),
        sa.Column("tasks_mapped", sa.Integer(), nullable=False),
        sa.Column("tasks_validated", sa.Integer(), nullable=False),
        sa.Column("tasks_bad_imagery", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["aoi_id"], ["areas_of_interest.id"]),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"], name="fk_users"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_projects_campaign_tag"), "projects", ["campaign_tag"], unique=False
    )
    op.create_index(
        op.f("ix_projects_mapper_level"), "projects", ["mapper_level"], unique=False
    )
    op.create_index(
        op.f("ix_projects_mapping_types"), "projects", ["mapping_types"], unique=False
    )
    op.create_index(
        op.f("ix_projects_organisation_tag"),
        "projects",
        ["organisation_tag"],
        unique=False,
    )
    op.create_table(
        "project_info",
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("locale", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=512), nullable=True),
        sa.Column("short_description", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("instructions", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("project_id", "locale"),
    )
    op.create_index(
        "idx_project_info composite",
        "project_info",
        ["locale", "project_id"],
        unique=False,
    )
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("x", sa.Integer(), nullable=False),
        sa.Column("y", sa.Integer(), nullable=False),
        sa.Column("zoom", sa.Integer(), nullable=False),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(geometry_type="MULTIPOLYGON", srid=4326),
            nullable=True,
        ),
        sa.Column("task_status", sa.Integer(), nullable=True),
        sa.Column("locked_by", sa.BigInteger(), nullable=True),
        sa.Column("mapped_by", sa.BigInteger(), nullable=True),
        sa.Column("validated_by", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(["locked_by"], ["users.id"], name="fk_users_locked"),
        sa.ForeignKeyConstraint(["mapped_by"], ["users.id"], name="fk_users_mapper"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(
            ["validated_by"], ["users.id"], name="fk_users_validator"
        ),
        sa.PrimaryKeyConstraint("id", "project_id"),
    )
    op.create_index(op.f("ix_tasks_project_id"), "tasks", ["project_id"], unique=False)
    op.create_table(
        "task_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("action_text", sa.String(), nullable=True),
        sa.Column("action_date", sa.DateTime(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(
            ["task_id", "project_id"], ["tasks.id", "tasks.project_id"], name="fk_tasks"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_users"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_task_history_composite",
        "task_history",
        ["task_id", "project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_task_history_project_id"), "task_history", ["project_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_task_history_project_id"), table_name="task_history")
    op.drop_index("idx_task_history_composite", table_name="task_history")
    op.drop_table("task_history")
    op.drop_index(op.f("ix_tasks_project_id"), table_name="tasks")
    op.drop_table("tasks")
    op.drop_index("idx_project_info composite", table_name="project_info")
    op.drop_table("project_info")
    op.drop_index(op.f("ix_projects_organisation_tag"), table_name="projects")
    op.drop_index(op.f("ix_projects_mapping_types"), table_name="projects")
    op.drop_index(op.f("ix_projects_mapper_level"), table_name="projects")
    op.drop_index(op.f("ix_projects_campaign_tag"), table_name="projects")
    op.drop_table("projects")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    op.drop_table("tags")
    op.drop_table("areas_of_interest")
    # ### end Alembic commands ###