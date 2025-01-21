#!/bin/bash

echo "Starting build process..."

# Print the PATH to check if the Python directory is included
echo "Current PATH: $PATH"

# Check Python version
python3 --version || { echo 'Python is not available'; exit 1; }

# Upgrade pip to the latest version
python3 -m pip install --upgrade pip || { echo 'Failed to upgrade pip'; exit 1; }

# Install only the required dependencies
python3 -m pip install --no-cache-dir -r requirements.txt || { echo 'Failed to install dependencies'; exit 1; }

# Ensure the static files output directory exists
mkdir -p staticfiles_build/static

# Run makemigrations to create any new migration files
python3 manage.py makemigrations || { echo 'Failed to make migrations'; exit 1; }

# Run the collectstatic command to gather all static files
python3 manage.py collectstatic --noinput || { echo 'Failed to collect static files'; exit 1; }

# Apply migrations to the database
python3 manage.py migrate || { echo 'Failed to apply migrations'; exit 1; }

echo "Build process completed successfully."
