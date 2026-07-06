#!/bin/bash
set -e

echo "Starting FastAPI application..."

# Run setup script to create media table
echo "Setting up database..."
python setup_media_table.py

# Start the application
echo "Starting uvicorn server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
