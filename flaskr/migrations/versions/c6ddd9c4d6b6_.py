"""empty message

Revision ID: c6ddd9c4d6b6
Revises: d9cd9f6735a0
Create Date: 2024-08-15 19:01:05.865078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6ddd9c4d6b6'
down_revision = 'd9cd9f6735a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('post_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('author_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id'),
    schema='public'
    )
    with op.batch_alter_table('likes_version', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_public_likes_version_end_transaction_id'), ['end_transaction_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_public_likes_version_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_public_likes_version_operation_type'), ['operation_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_public_likes_version_transaction_id'), ['transaction_id'], unique=False)

    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.drop_constraint('comments_author_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('comments_post_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['author_id'], ['id'], referent_schema='public', ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'posts', ['post_id'], ['id'], referent_schema='public', ondelete='CASCADE')

    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.drop_constraint('likes_author_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('likes_post_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'posts', ['post_id'], ['id'], referent_schema='public', ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'users', ['author_id'], ['id'], referent_schema='public', ondelete='CASCADE')

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint('posts_author_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['author_id'], ['id'], referent_schema='public', ondelete='CASCADE')

    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_constraint('transaction_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'], referent_schema='public')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('transaction_user_id_fkey', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('posts_author_id_fkey', 'users', ['author_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('likes_post_id_fkey', 'posts', ['post_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key('likes_author_id_fkey', 'users', ['author_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('comments_post_id_fkey', 'posts', ['post_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key('comments_author_id_fkey', 'users', ['author_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('likes_version', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_public_likes_version_transaction_id'))
        batch_op.drop_index(batch_op.f('ix_public_likes_version_operation_type'))
        batch_op.drop_index(batch_op.f('ix_public_likes_version_id'))
        batch_op.drop_index(batch_op.f('ix_public_likes_version_end_transaction_id'))

    op.drop_table('likes_version', schema='public')
    # ### end Alembic commands ###
