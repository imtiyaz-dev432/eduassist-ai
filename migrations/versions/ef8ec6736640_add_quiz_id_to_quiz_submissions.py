"""add student id to quiz submission answers

Revision ID: ef8ec6736640
Revises: 58e8c63d8433
Create Date: 2026-06-07 13:04:18.662306

"""
from alembic import op
import sqlalchemy as sa


revision = 'ef8ec6736640'
down_revision = '58e8c63d8433'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('quiz_submission_answers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student_id', sa.Integer(), nullable=True))

    op.execute("""
        UPDATE quiz_submission_answers AS qsa
        SET student_id = qs.student_id
        FROM quiz_submissions AS qs
        WHERE qsa.quiz_submission_id = qs.id
    """)

    with op.batch_alter_table('quiz_submission_answers', schema=None) as batch_op:
        batch_op.alter_column('student_id', nullable=False)
        batch_op.create_foreign_key(
            'fk_quiz_submission_answers_student_id',
            'students',
            ['student_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('quiz_submission_answers', schema=None) as batch_op:
        batch_op.drop_constraint(
            'fk_quiz_submission_answers_student_id',
            type_='foreignkey'
        )
        batch_op.drop_column('student_id')