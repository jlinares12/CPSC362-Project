"""Made the longitude and latitude attributes to float

Revision ID: 81294aa90734
Revises: 2cc2e96ffdbd
Create Date: 2025-03-14 12:02:49.594264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81294aa90734'
down_revision = '2cc2e96ffdbd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('garden', schema=None) as batch_op:
        batch_op.alter_column('latitude',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
        batch_op.alter_column('longitude',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('garden', schema=None) as batch_op:
        batch_op.alter_column('longitude',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('latitude',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
