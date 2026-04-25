#!/bin/bash

# AI-Powered Talent Scouting Agent - Startup Script

echo "AI-Powered Talent Scouting Agent - Starting Up"
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p data/logs data/cache

# Start the application
echo "Starting the application..."
python main.py

echo "Application started successfully!"