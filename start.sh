#!/bin/bash

# Startup script for the Document to Floify API

echo "Starting Document to Floify API..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "No .env file found. Creating from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Created .env from example. Please edit it to add your API keys."
        echo "IMPORTANT: You need to add your LANDINGAI_API_KEY and MISTRAL_API_KEY to the .env file."
        exit 1
    else
        echo "Error: No .env.example file found. Cannot create .env."
        exit 1
    fi
fi

# Install dependencies if needed
echo "Checking dependencies..."
pip3 install -r requirements.txt > /dev/null 2>&1

# Start the API
echo "Launching API on port $(grep PORT .env | cut -d= -f2 || echo 7777)..."
python3 app.py 