#!/bin/bash

# Startup script for the Document to Floify API

echo "Starting Document to Floify API..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Install dependencies if needed
echo "Checking dependencies..."
pip3 install -r requirements.txt > /dev/null 2>&1

# Start the API
echo "Launching API on port 7777..."
python3 app.py 