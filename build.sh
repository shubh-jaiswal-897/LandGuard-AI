#!/bin/bash

# Build script for Vercel deployment
echo "Building project..."

# Install dependencies
python3 -m pip install -r requirements.txt --break-system-packages

# Run migrations (Optional: better to do it manually if using external DB)
# python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput
