#!/bin/bash

# Build script for Vercel deployment
echo "Building project..."

# Install dependencies
python -m pip install -r requirements.txt

# Run migrations (Optional: better to do it manually if using external DB)
# python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
