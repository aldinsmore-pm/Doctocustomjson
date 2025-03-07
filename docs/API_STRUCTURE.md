# Document to Floify API Structure

## Components

The API consists of the following components:

1. **Flask API Server (`app.py`)**
   - Provides the HTTP endpoints
   - Receives document URLs from clients
   - Calls the document processing pipeline
   - Returns the processed Floify JSON

2. **Document to Floify Pipeline (`scripts/document_to_floify_pipeline.py`)**
   - Handles document downloading and processing
   - Calls Landing.ai for OCR processing
   - Uses Mistral LLM to transform text to Floify format
   - Saves processing results to output directories

3. **Support Scripts**
   - `start.sh`: Launches the API
   - `setup_ngrok.sh`: Exposes the API via ngrok
   - `tests/test_api.sh`: Tests the API functionality

## API Flow

1. Client sends a document URL to `/process-document`
2. `app.py` validates the request and calls `process_document_to_floify`
3. The pipeline downloads the document (if it's a URL)
4. The document is sent to Landing.ai for OCR processing
5. Landing.ai returns text and structural information
6. The extracted text is sent to Mistral LLM for transformation
7. Mistral LLM transforms the text to Floify 1003 JSON format
8. The API returns the Floify JSON to the client

## Data Flow Diagram

```
Client -> API (app.py) -> Document Pipeline -> Landing.ai OCR
                                            -> Mistral LLM
                                            -> Floify JSON
                                            -> Output Directory
      <- Response with Floify JSON       <-
```

## Architecture Decisions

1. **Flask vs FastAPI**: Flask was chosen for simplicity and ease of implementation
2. **Landing.ai vs Other OCR**: Landing.ai provides accurate text extraction with structural understanding
3. **Mistral LLM**: Used for its ability to transform unstructured text into specific JSON formats
4. **Output Directories**: Each document processing creates a timestamped directory to store all outputs for debugging and auditing

## Scalability Considerations

For higher scale deployments, consider:

1. Adding a database to store processing results
2. Implementing a queue system for document processing
3. Setting up multiple worker instances
4. Adding authentication and rate limiting 