# Document to Floify API

A RESTful API service that processes mortgage documents (from URLs) and converts them to Floify 1003 JSON format.

## Features

- Process documents via URL (PDFs and images)
- Extract text with high accuracy using Landing.ai OCR
- Transform OCR results into structured Floify 1003 JSON format
- Simple RESTful API interface
- Accessible both locally and remotely via ngrok

## API Endpoints

### Health Check

```
GET /health
```

Returns a simple status check to verify the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

### Process Document

```
POST /process-document
```

Processes a document from a URL and returns the Floify 1003 JSON format.

**Request:**
```json
{
  "document_url": "https://example.com/path/to/document.pdf"
}
```

**Response:**
A structured Floify 1003 JSON object containing extracted information.

## Current Deployment

The API is currently running and accessible at:

```
https://e40a-2600-6c67-68f0-8eb0-502c-294a-5ec1-8628.ngrok-free.app
```

Example usage with curl:

```bash
# Health check
curl https://e40a-2600-6c67-68f0-8eb0-502c-294a-5ec1-8628.ngrok-free.app/health

# Process document
curl -X POST \
     https://e40a-2600-6c67-68f0-8eb0-502c-294a-5ec1-8628.ngrok-free.app/process-document \
     -H "Content-Type: application/json" \
     -d '{"document_url": "https://example.com/path/to/document.pdf"}'
```

## Local Setup

If you need to run the API locally:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the API server:
```bash
python app.py
```

This will start the server on port 7777.

## Exposing via ngrok

The API is already exposed via ngrok, but if you need to restart it:

1. Make sure the API is running locally on port 7777
2. Run the ngrok setup script:
```bash
./setup_ngrok.sh
```

Note: The free ngrok account is limited to 1 simultaneous tunnel. If you get an error about this limitation, visit https://dashboard.ngrok.com/agents to manage your active tunnels.

## How It Works

The API uses a two-step process:

1. **Document Processing**: Uses Landing.ai's Document Analysis API to extract text and structure from the document
2. **Transformation**: Uses Mistral LLM to convert the extracted content into Floify 1003 JSON format

Processing times typically range from 2-5 minutes depending on document complexity.

## Output

For each document processed, the API creates a directory with:

- `landingai_results.json`: Raw results from Landing.ai OCR
- `extracted_text.txt`: Extracted text from the document
- `llm_response.txt`: Raw response from Mistral LLM
- `floify_1003.json`: Final structured Floify 1003 JSON

## Testing

A test script is provided in the `tests` directory:

```bash
./tests/test_api.sh
```

This tests the API with a simple PDF document.

## Limitations

- Processing time depends on document complexity and API response times
- Landing.ai has a limit of 2 pages per PDF
- The API requires the document URL to be publicly accessible 