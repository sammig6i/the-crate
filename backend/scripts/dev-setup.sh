#!/bin/bash

# Ensure we're in the backend directory
cd "$(dirname "$0")/.." || exit

# Run database migrations
echo "Running database migrations..."
alembic upgrade head


# Seed the database
echo "Seeding the database..."
python -m app.db.seed

echo "Development environment setup complete!" 