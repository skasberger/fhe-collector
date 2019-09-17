"""add is_valid to Doi()

Revision ID: 776edda4b9fa
Revises: 4ee0b4c33912
Create Date: 2019-08-09 13:12:15.455544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '776edda4b9fa'
down_revision = '4ee0b4c33912'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('api_request')
    op.add_column('doi', sa.Column('is_valid', sa.Boolean(), nullable=True))
    op.drop_column('doi', 'unpaywall')
    op.drop_column('doi', 'ncbi')
    op.drop_column('doi', 'doi_old')
    op.drop_column('doi', 'doi_new')
    op.drop_column('doi', 'doi_lp')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('doi', sa.Column('doi_lp', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('doi', sa.Column('doi_new', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('doi', sa.Column('doi_old', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('doi', sa.Column('ncbi', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('doi', sa.Column('unpaywall', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('doi', 'is_valid')
    op.create_table('api_request',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('url', sa.VARCHAR(length=512), autoincrement=False, nullable=False),
    sa.Column('request_url', sa.VARCHAR(length=512), autoincrement=False, nullable=True),
    sa.Column('request_type', sa.VARCHAR(length=32), autoincrement=False, nullable=True),
    sa.Column('response', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=32), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['url'], ['url.url'], name='api_request_url_fkey'),
    sa.PrimaryKeyConstraint('id', name='api_request_pkey')
    )
    # ### end Alembic commands ###