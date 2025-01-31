from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '42d59b265707'
down_revision = '6bf5a7152455'
branch_labels = None
depends_on = None


def upgrade():
    # Rename tables instead of dropping them
    op.rename_table('areas', 'area')
    op.rename_table('shows', 'show')

    # Adjust foreign key constraints
    op.drop_constraint('artist_area_id_fkey', 'artist', type_='foreignkey')
    op.create_foreign_key(None, 'artist', 'area', ['area_id'], ['id'])
    op.drop_constraint('venue_area_id_fkey', 'venue', type_='foreignkey')
    op.create_foreign_key(None, 'venue', 'area', ['area_id'], ['id'])


def downgrade():
    # Rename tables back to their original names
    op.rename_table('area', 'areas')
    op.rename_table('show', 'shows')

    # Adjust foreign key constraints
    op.drop_constraint(None, 'venue', type_='foreignkey')
    op.create_foreign_key('venue_area_id_fkey', 'venue',
                          'areas', ['area_id'], ['id'])
    op.drop_constraint(None, 'artist', type_='foreignkey')
    op.create_foreign_key('artist_area_id_fkey', 'artist',
                          'areas', ['area_id'], ['id'])
