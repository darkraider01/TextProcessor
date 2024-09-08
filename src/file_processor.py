import os
import json
import logging
from text_analysis import TextAnalysis
from text_extraction import TextExtractor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_processed_files(log_file):
    """Load the list of processed files from the JSON log file."""
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as file:
                return set(json.load(file))
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from log file '{log_file}': {e}")
    return set()

def save_processed_file(file_name, log_file):
    """Save a processed file's name to the JSON log file."""
    processed_files = load_processed_files(log_file)
    processed_files.add(file_name)
    try:
        with open(log_file, 'w', encoding='utf-8') as file:
            json.dump(list(processed_files), file, indent=4)
    except IOError as e:
        logging.error(f"Error writing to log file '{log_file}': {e}")

def analyze_and_save(file_path, output_dir, log_file, filter_file=None):
    """Analyze a file and save the extracted text and analysis results to a JSON file in the specified output directory."""
    try:
        file_name = os.path.basename(file_path)

        # Skip if file has already been processed
        if file_name in load_processed_files(log_file):
            logging.info(f"Skipping already processed file: {file_name}")
            return

        extracted_text = ""
        analysis_results = {}

        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            # Extract text from image
            extractor = TextExtractor()
            results = extractor.process_image(file_path)
            
            if not results:
                logging.error(f"No text extracted from image {file_path}.")
                return
            
            # Combine extracted text from all areas
            extracted_text = "\n".join([res['text'] for res in results])
            logging.info(f"Extracted text from image {file_path}: '{extracted_text}'")

        elif file_path.lower().endswith(('.json', '.txt')):
            # Read text from file
            if file_path.lower().endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    extracted_text = json.dumps(data)  # Convert JSON to string
            elif file_path.lower().endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    extracted_text = file.read()

        else:
            logging.error(f"Unsupported file type: {file_path}. Supported types are image files, JSON files, and text files.")
            return

        # Perform text analysis on the extracted or read text
        analysis = TextAnalysis(filter_file=filter_file)  # Pass filter file path
        analysis_results = analysis.analyze_text(extracted_text)

        # Prepare results for saving
        results = {
            'extracted_text': extracted_text,
            'analysis_results': analysis_results
        }

        # Save results to JSON file
        output_file = os.path.join(output_dir, f"{file_name}_analysis.json")
        os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
        
        # Debugging log
        logging.info(f"Saving results to: {output_file}")

        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(results, json_file, indent=4)
        
        logging.info(f"Results saved to {output_file}")

        # Update processed files log
        save_processed_file(file_name, log_file)

    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
