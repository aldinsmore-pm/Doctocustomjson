from flask import Flask, request, jsonify
import os
import json
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
from document_to_floify_pipeline import process_document_to_floify

app = Flask(__name__)

@app.route('/process-document', methods=['POST'])
def process_document():
    try:
        print("Received request to /process-document")
        data = request.get_json()
        print(f"Request data: {data}")
        
        if not data or 'document_url' not in data:
            print("Missing document_url in request")
            return jsonify({"error": "Missing document_url"}), 400
        
        document_url = data['document_url']
        print(f"Processing document URL: {document_url}")
        
        # Process the document using your existing function
        output_dir = process_document_to_floify(document_url)
        print(f"Document processed, output directory: {output_dir}")
        
        # Read the Floify JSON from the output directory
        floify_file = f"{output_dir}/floify_1003.json"
        if not os.path.exists(floify_file):
            print(f"Floify JSON file not found: {floify_file}")
            return jsonify({"error": "Failed to generate Floify JSON"}), 500
        
        with open(floify_file, 'r') as f:
            floify_json = json.load(f)
        
        print("Successfully returning Floify JSON")
        return jsonify(floify_json)
    except Exception as e:
        import traceback
        print(f"Error processing document: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/', methods=['GET'])
def root():
    return "Document to Floify API is running. Use /process-document endpoint for document processing."

if __name__ == '__main__':
    # Get configuration from environment variables
    PORT = int(os.getenv('PORT', 7777))
    HOST = os.getenv('HOST', '0.0.0.0')
    DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'
    
    print(f"Starting server on {HOST}:{PORT}")
    print(f"To test the API, use: curl -X POST http://{HOST if HOST != '0.0.0.0' else 'localhost'}:{PORT}/process-document -H \"Content-Type: application/json\" -d '{{\"document_url\": \"https://example.com/sample.pdf\"}}'")
    
    app.run(host=HOST, port=PORT, debug=DEBUG) 