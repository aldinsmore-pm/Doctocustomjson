#!/bin/bash

# Script to test the API endpoint
echo "Testing document processing API endpoint..."

# URL to test
TEST_URL="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

# Test local API
echo "Testing local API..."
curl -X POST http://localhost:7777/process-document \
     -H "Content-Type: application/json" \
     -d "{\"document_url\": \"$TEST_URL\"}"

echo
echo

# Test remote API via ngrok
echo "Testing remote API via ngrok..."
curl -X POST https://e40a-2600-6c67-68f0-8eb0-502c-294a-5ec1-8628.ngrok-free.app/process-document \
     -H "Content-Type: application/json" \
     -d "{\"document_url\": \"$TEST_URL\"}"

echo
echo "Test completed" 