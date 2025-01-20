
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

python3.9 manage.py collectstatic --noinput

# Apply migrations (if using Django)
python3 manage.py migrate || { echo 'Failed to apply migrations'; exit 1; }

echo "Build process completed successfully."
