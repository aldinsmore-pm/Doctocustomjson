#!/bin/bash

# Script to set up and run ngrok for the document-to-floify API
echo "Setting up ngrok for the document-to-floify API (port 7777)..."

# Check if ngrok is already installed
if ! command -v ngrok &> /dev/null; then
    echo "ngrok not found. Installing..."
    
    # Download ngrok based on architecture
    if [[ $(uname -m) == "arm64" ]]; then
        # ARM64 architecture (Apple Silicon)
        curl -O https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-arm64.zip
        unzip ngrok-v3-stable-darwin-arm64.zip
        rm ngrok-v3-stable-darwin-arm64.zip
    else
        # Intel architecture
        curl -O https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.zip
        unzip ngrok-v3-stable-darwin-amd64.zip
        rm ngrok-v3-stable-darwin-amd64.zip
    fi
    
    echo "ngrok downloaded to the current directory."
    
    # Make it executable and move to a location in PATH (optional)
    chmod +x ./ngrok
    echo "You may want to move ngrok to a location in your PATH, e.g.:"
    echo "sudo mv ./ngrok /usr/local/bin/"
    
    # Set up ngrok path for this session
    NGROK_PATH="./ngrok"
else
    NGROK_PATH="ngrok"
    echo "ngrok is already installed."
fi

# Remind about authentication
echo ""
echo "IMPORTANT: Before using ngrok, you need to authenticate with your auth token."
echo "If you haven't done this yet, run the following command:"
echo "${NGROK_PATH} authtoken YOUR_AUTH_TOKEN"
echo ""
echo "Replace YOUR_AUTH_TOKEN with the token from your ngrok account."
echo ""

# Run ngrok on the correct port (7777)
echo "Starting ngrok to expose port 7777..."
echo "This will create a public URL for your document-to-floify API."
echo ""
echo "Running: ${NGROK_PATH} http 7777"
echo ""
echo "When ngrok starts, it will display the public URL your team can use."
echo "Example API usage: https://your-ngrok-url.ngrok.io/process-document"
echo ""

# Start ngrok
${NGROK_PATH} http 7777 