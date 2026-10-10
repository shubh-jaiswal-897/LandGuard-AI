#!/bin/bash

# Build script for Vercel deployment
echo "Building project..."

# Install dependencies
python3 -m pip install -r requirements.txt --break-system-packages

# Run migrations
python3 manage.py migrate

# Seed database & create administrator shubh1111
python3 populate_db.py

# Collect static files
python3 manage.py collectstatic --noinput
