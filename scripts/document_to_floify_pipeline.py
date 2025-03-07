#!/usr/bin/env python3
"""
Document to Floify Pipeline

This script provides a streamlined workflow to:
1. Process a document (local file or URL) using Landing.ai OCR
2. Transform the OCR results into structured Floify JSON format using Mistral LLM
"""

import os
import json
import time
import requests
import urllib.parse
from datetime import datetime
from mistralai import Mistral

# Configuration
LANDINGAI_API_KEY = "OWx6bWd0c3JpNGI2YTk2bDN3OHF3OlJ5NVJqUGFWb3VwbDM4ZjlEVmJvVEp6cjA1TTdmdnc3"
MISTRAL_API_KEY = "68T0CBWpmreNywJa25eHmxb37xRhKlVO"
LANDINGAI_URL = "https://api.va.landing.ai/v1/tools/agentic-document-analysis"
MISTRAL_MODEL = "mistral-large-latest"  # LLM model

# Initialize Mistral client
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

def is_url(path):
    """Check if a string is a URL"""
    try:
        result = urllib.parse.urlparse(path)
        return all([result.scheme, result.netloc])
    except:
        return False

def download_document(url):
    """
    Download a document from a URL
    
    Args:
        url: URL to the document
        
    Returns:
        tuple: (content, filename)
    """
    print(f"Downloading document from URL: {url}")
    try:
        # Get the filename from the URL
        filename = url.split('/')[-1]
        if not filename:
            filename = "document.pdf"  # Default filename
            
        # Add extension if missing
        if '.' not in filename:
            filename += ".pdf"  # Default extension
            
        # Download the document
        response = requests.get(url, timeout=180)
        response.raise_for_status()  # Raise an error if the download fails
        
        print(f"Download completed: {len(response.content)} bytes")
        return response.content, filename
    except Exception as e:
        print(f"Error downloading document: {str(e)}")
        return None, None

def process_document_with_landingai(document_path):
    """
    Process a document using Landing.ai OCR
    
    Args:
        document_path: Path to the document or URL
        
    Returns:
        dict: The OCR results from Landing.ai
    """
    # Check if path is a URL
    is_document_url = is_url(document_path)
    
    if is_document_url:
        print(f"Processing document URL with Landing.ai: {document_path}")
        
        # Download the document
        document_content, filename = download_document(document_path)
        if not document_content:
            raise Exception(f"Failed to download document from URL: {document_path}")
        
        # Determine file type from filename
        file_extension = os.path.splitext(filename)[1].lower()
        
        # Prepare request
        headers = {
            "Authorization": f"Basic {LANDINGAI_API_KEY}"
        }
        
        # Set up the appropriate file parameter based on file type
        if file_extension in ['.pdf']:
            files = {"pdf": (filename, document_content)}
        else:  # Default to image for png, jpg, etc.
            files = {"image": (filename, document_content)}
    else:
        print(f"Processing local document with Landing.ai: {document_path}")
        
        # Check if file exists
        if not os.path.exists(document_path):
            raise FileNotFoundError(f"Document not found: {document_path}")
        
        # Determine file type
        file_extension = os.path.splitext(document_path)[1].lower()
        
        # Prepare request
        headers = {
            "Authorization": f"Basic {LANDINGAI_API_KEY}"
        }
        
        # Set up the appropriate file parameter based on file type
        if file_extension in ['.pdf']:
            files = {"pdf": open(document_path, "rb")}
        else:  # Default to image for png, jpg, etc.
            files = {"image": open(document_path, "rb")}
    
    try:
        print("Sending request to Landing.ai (this may take 2-5 minutes)...")
        start_time = time.time()
        
        # Send request with 10 minute timeout
        response = requests.post(
            LANDINGAI_URL,
            headers=headers,
            files=files,
            timeout=600  # 10 minute timeout
        )
        
        # Close file handles if local file
        if not is_document_url:
            for f in files.values():
                f.close()
        
        elapsed_time = time.time() - start_time
        print(f"Landing.ai request completed in {elapsed_time:.2f} seconds")
        
        # Check for successful response
        if response.status_code == 200:
            ocr_results = response.json()
            return ocr_results
        else:
            print(f"Error from Landing.ai API: Status {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error processing document with Landing.ai: {str(e)}")
        # Ensure file handles are closed if local file
        if not is_document_url:
            for f in files.values():
                if hasattr(f, 'close'):
                    f.close()
        return None

def extract_text_from_landingai(landingai_data):
    """
    Extract the markdown text from Landing.ai results
    
    Args:
        landingai_data: The OCR results from Landing.ai
        
    Returns:
        str: The extracted text
    """
    if not landingai_data:
        return ""
        
    if "data" in landingai_data and "markdown" in landingai_data["data"]:
        return landingai_data["data"]["markdown"]
    
    # If we don't have the expected structure, try to extract text from chunks
    if "data" in landingai_data and "chunks" in landingai_data["data"]:
        text = ""
        for chunk in landingai_data["data"]["chunks"]:
            if "text" in chunk:
                text += chunk["text"] + "\n\n"
        return text
        
    return ""

def transform_to_floify_with_llm(text):
    """
    Use Mistral LLM to transform the OCR text into Floify JSON format
    
    Args:
        text: The OCR text to transform
        
    Returns:
        tuple: (floify_json, llm_response)
    """
    # Create a comprehensive prompt that ensures we extract all available fields
    prompt = f"""
You are an expert document analyzer specializing in mortgage applications. Extract ALL available information from the OCR text below and format it into a complete Floify 1003 JSON structure.

The OCR text from the document is:
```
{text}
```

Create a comprehensive Floify 1003 JSON with these sections:
1. Borrower information:
   - Personal details (name, contact info)
   - Current address
   - Detailed employment history (all employers with dates, positions, and income)
   - Income breakdowns (base, overtime, bonuses, commissions) with frequencies
   - All assets and liabilities mentioned

2. Co-borrower information (if present):
   - Same detailed structure as borrower

3. Property information:
   - Address, property type, and usage details

4. Loan information:
   - Loan amount, type, term, interest rate, and purpose

Be thorough and extract every piece of information available in the document. For fields not present in the text, use null values.

Format the response as a complete, well-structured JSON object following the Floify 1003 format with all nested objects and arrays properly structured.

Return ONLY the JSON object without any explanations.
"""
    
    # Send request to Mistral
    start_time = time.time()
    print("Sending request to Mistral LLM...")
    
    # Using the correct chat.complete method
    response = mistral_client.chat.complete(
        model=MISTRAL_MODEL,
        messages=[
            {"role": "system", "content": "You are a specialized document extraction assistant that transforms OCR text into structured Floify 1003 JSON format with complete comprehensive extraction of all available fields."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,  # Use deterministic output for consistent extraction
        max_tokens=4000
    )
    
    elapsed_time = time.time() - start_time
    print(f"LLM request completed in {elapsed_time:.2f} seconds")
    
    # Extract the JSON from the response
    llm_response = response.choices[0].message.content
    
    # Clean up the response to extract just the JSON
    if "```json" in llm_response:
        # Extract JSON content between code blocks
        json_str = llm_response.split("```json")[1].split("```")[0].strip()
    elif "```" in llm_response:
        # Extract content between generic code blocks
        json_str = llm_response.split("```")[1].split("```")[0].strip()
    else:
        # Use the whole response
        json_str = llm_response.strip()
    
    try:
        # Parse the JSON to ensure it's valid
        floify_json = json.loads(json_str)
        return floify_json, llm_response
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from LLM response: {e}")
        print(f"Raw LLM response: {llm_response}")
        return None, llm_response

def process_document_to_floify(document_path, output_dir=None):
    """
    Complete pipeline to process document to Floify JSON
    
    Args:
        document_path: Path to the document or URL
        output_dir: Directory to save output files (default: auto-generate)
        
    Returns:
        str: Path to the output directory
    """
    # Create timestamp for unique output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Check if path is a URL
    is_document_url = is_url(document_path)
    
    if is_document_url:
        # For URLs, use the last part of the URL as the base name
        document_name = document_path.split('/')[-1]
        if not document_name:
            document_name = "url_document"
        document_base = document_name
    else:
        # For local files, use the file base name
        document_name = os.path.basename(document_path)
        document_base = os.path.splitext(document_name)[0]
    
    # Create output directory if not provided
    if not output_dir:
        output_dir = f"output_{document_base}_{timestamp}"
        
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output will be saved to: {output_dir}")
    
    # Step 1: Process document with Landing.ai
    landingai_results = process_document_with_landingai(document_path)
    
    if not landingai_results:
        print("Failed to process document with Landing.ai")
        return output_dir
    
    # Save Landing.ai results
    landingai_results_file = os.path.join(output_dir, "landingai_results.json")
    with open(landingai_results_file, "w") as f:
        json.dump(landingai_results, f, indent=2)
    print(f"Landing.ai results saved to: {landingai_results_file}")
    
    # Step 2: Extract text from Landing.ai results
    ocr_text = extract_text_from_landingai(landingai_results)
    
    # Save extracted text
    text_file = os.path.join(output_dir, "extracted_text.txt")
    with open(text_file, "w") as f:
        f.write(ocr_text)
    print(f"Extracted text saved to: {text_file}")
    
    # Step 3: Transform to Floify JSON using LLM
    floify_json, llm_response = transform_to_floify_with_llm(ocr_text)
    
    # Save LLM response
    llm_response_file = os.path.join(output_dir, "llm_response.txt")
    with open(llm_response_file, "w") as f:
        f.write(llm_response)
    print(f"LLM response saved to: {llm_response_file}")
    
    if floify_json:
        # Save Floify JSON
        floify_file = os.path.join(output_dir, "floify_1003.json")
        with open(floify_file, "w") as f:
            json.dump(floify_json, f, indent=2)
        print(f"Floify JSON saved to: {floify_file}")
        
        # Print a small preview
        print("\nFloify JSON Preview:")
        preview = json.dumps(floify_json, indent=2)
        print(preview[:500] + "..." if len(preview) > 500 else preview)
    else:
        print("Failed to generate valid Floify JSON")
    
    return output_dir

def main():
    """Main function to process a document to Floify JSON"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Process a document to Floify JSON")
    parser.add_argument("document_path", help="Path to the document or document URL")
    parser.add_argument("--output-dir", help="Directory to save output files")
    
    args = parser.parse_args()
    
    process_document_to_floify(args.document_path, args.output_dir)

if __name__ == "__main__":
    main() 