#!/bin/bash

# Script to test the API endpoint
echo "Testing document processing API endpoint..."

# Load environment variables if available
if [ -f "../.env" ]; then
    source "../.env"
fi

# Set default values if not in environment
PORT=${PORT:-7777}
HOST=${HOST:-0.0.0.0}
NGROK_URL=${NGROK_URL:-https://e40a-2600-6c67-68f0-8eb0-502c-294a-5ec1-8628.ngrok-free.app}

# URL to test
TEST_URL="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

# Test local API
echo "Testing local API on http://localhost:${PORT}..."
curl -X POST http://localhost:${PORT}/process-document \
     -H "Content-Type: application/json" \
     -d "{\"document_url\": \"$TEST_URL\"}"

echo
echo

# Test remote API via ngrok
echo "Testing remote API via ${NGROK_URL}..."
curl -X POST ${NGROK_URL}/process-document \
     -H "Content-Type: application/json" \
     -d "{\"document_url\": \"$TEST_URL\"}"

echo
echo "Test completed" 