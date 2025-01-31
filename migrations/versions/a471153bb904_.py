from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a471153bb904'
down_revision = '8b96b315ccd4'
branch_labels = None
depends_on = None


def upgrade():
    # Create the 'areas' table
    op.create_table(
        'areas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('city', sa.String(length=120), nullable=False),
        sa.Column('state', sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Insert a default area record
    op.execute(
        "INSERT INTO areas (id, city, state) VALUES (1, 'Default City', 'Default State')")

    # Alter 'shows' table columns to be non-nullable
    op.alter_column('shows', 'artist_id',
                    existing_type=sa.INTEGER(), nullable=False)
    op.alter_column('shows', 'venue_id',
                    existing_type=sa.INTEGER(), nullable=False)

    # Add 'area_id' column with a default value for existing records
    op.add_column('venue', sa.Column('area_id', sa.Integer(), nullable=True))
    # Ensure no null values
    op.execute('UPDATE venue SET area_id = 1 WHERE area_id IS NULL')
    # Make the column non-nullable
    op.alter_column('venue', 'area_id', nullable=False)

    # Create foreign key constraint
    op.create_foreign_key(None, 'venue', 'areas', ['area_id'], ['id'])

    # Drop 'state' and 'city' columns from 'venue'
    op.drop_column('venue', 'state')
    op.drop_column('venue', 'city')


def downgrade():
    # Add 'state' and 'city' columns back to 'venue'
    op.add_column('venue', sa.Column('city', sa.VARCHAR(
        length=120), autoincrement=False, nullable=False))
    op.add_column('venue', sa.Column('state', sa.VARCHAR(
        length=120), autoincrement=False, nullable=False))

    # Drop foreign key constraint and 'area_id' column
    op.drop_constraint(None, 'venue', type_='foreignkey')
    op.drop_column('venue', 'area_id')

    # Alter 'shows' table columns to be nullable
    op.alter_column('shows', 'venue_id',
                    existing_type=sa.INTEGER(), nullable=True)
    op.alter_column('shows', 'artist_id',
                    existing_type=sa.INTEGER(), nullable=True)

    # Drop the 'areas' table
    op.drop_table('areas')
