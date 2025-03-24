# Alembic Migration Guide

This guide provides instructions for generating Alembic migrations and handling Enum types when modifying database schemas.

## Generating Migrations

### Auto-Detect Changes
To create a migration with automatically detected changes:

```bash
alembic revision --autogenerate -m "Your message"
```

### Create an Empty Migration
To generate a blank migration script:

```bash
alembic revision -m "Your message"
```

## Applying and Reverting Migrations

### Upgrade to the Latest Version
To apply all pending migrations:

```bash
alembic upgrade head
```

### Downgrade to the Previous Migration
To revert the most recent migration:

```bash
alembic downgrade -1
```

### Downgrade to a Specific Migration
To revert to a specific migration version:

```bash
alembic downgrade <revision_id>
```
Replace `<revision_id>` with the migration’s unique identifier.

## Handling Enum Types in Migrations

When working with Enum types, ensure proper ordering of column and type changes to prevent errors.

### Example Migration for Enum Handling

```python
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Enum

def upgrade():
    # Define Enum type
    my_enum = Enum('option1', 'option2', 'option3', name='my_enum_type')
    my_enum.create(op.get_bind(), checkfirst=True)
    
    # Add column with Enum type
    op.add_column('my_table', sa.Column('my_enum_column', my_enum, nullable=False, server_default='option1'))

def downgrade():
    # Remove column first
    op.drop_column('my_table', 'my_enum_column')
    
    # Drop Enum type safely
    op.execute("DROP TYPE IF EXISTS my_enum_type")
```

### Key Considerations:
- **Upgrade Process:**
  - Create the Enum type before adding the column.
  - Set a default value to avoid conflicts.
- **Downgrade Process:**
  - Drop the column first before removing the Enum type.
  - Use `DROP TYPE IF EXISTS` to avoid errors if the type does not exist.

Following these best practices ensures seamless migration handling, minimizing database inconsistencies.

