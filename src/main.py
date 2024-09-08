import os
import datetime
import uuid
import logging
from file_processor import analyze_and_save

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_filtered_words(path):
    """Load the filtered words from a text file."""
    try:
        with open(path, 'r', encoding='utf-8') as file:
            words = {line.strip().lower() for line in file if line.strip()}
        return words
    except Exception as e:
        logging.error(f"Error loading filtered words from '{path}': {e}")
        return set()

def main():
    """Main function to process files and save results."""
    # Retrieve directory paths from environment variables
    file_directory = os.getenv('FILE_DIRECTORY', 'C:/path/to/default/directory')
    output_directory = os.getenv('OUTPUT_DIRECTORY', 'C:/path/to/output/directory')
    processed_files_log = os.getenv('PROCESSED_FILES_LOG', 'processed_files.json')
    filtered_words_path = os.getenv('FILTERED_WORDS_PATH', 'C:/Users/brand/Downloads/negative-words.txt')

    # Log retrieved paths
    logging.info(f"File directory: {file_directory}")
    logging.info(f"Output directory: {output_directory}")
    logging.info(f"Processed files log: {processed_files_log}")
    logging.info(f"Filtered words path: {filtered_words_path}")

    if not os.path.exists(file_directory):
        logging.error(f"Directory '{file_directory}' does not exist.")
        return

    if not os.path.exists(filtered_words_path):
        logging.error(f"Filtered words file '{filtered_words_path}' does not exist.")
        return

    # Load filtered words
    filtered_words = load_filtered_words(filtered_words_path)
    if not filtered_words:
        logging.error("No filtered words loaded. Exiting.")
        return

    # Generate a unique folder name for this run
    now = datetime.datetime.now()
    timestamp = now.strftime("%d-%m-%Y_%H-%M")
    unique_run_folder = f"run_{timestamp}_{uuid.uuid4().hex}"
    unique_output_dir = os.path.join(output_directory, unique_run_folder)

    # Create the unique run directory
    os.makedirs(unique_output_dir, exist_ok=True)
    logging.info(f"Results will be saved in folder: {unique_output_dir}")

    # Process files in the source directory and its subdirectories
    for root, dirs, files in os.walk(file_directory):
        logging.info(f"Scanning directory: {root}")
        for file_name in files:
            source_file = os.path.join(root, file_name)

            # Log the file being processed
            logging.info(f"Processing file: {source_file}")
            try:
                analyze_and_save(source_file, unique_output_dir, processed_files_log, filter_file=filtered_words_path)
            except Exception as e:
                logging.error(f"Error processing file {source_file}: {e}")

if __name__ == "__main__":
    main()
