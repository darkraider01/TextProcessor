import os
import logging
from file_processor import analyze_and_save

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_files(source_dir, exclude_files=None, output_dir=None):
    """Process files from the source directory and its subdirectories based on exclusion criteria."""
    try:
        # Check if source directory exists
        if not os.path.exists(source_dir):
            logging.error(f"Source directory '{source_dir}' does not exist.")
            return

        # Walk through all directories and files
        for root, dirs, files in os.walk(source_dir):
            logging.info(f"Scanning directory: {root}")
            for dir in dirs:
                # Recursively process subdirectories
                sub_dir = os.path.join(root, dir)
                process_files(sub_dir, exclude_files, output_dir)

            for file_name in files:
                source_file = os.path.join(root, file_name)
                
                # Check if file is in the exclusion list
                if exclude_files and file_name in exclude_files:
                    logging.info(f"Skipping excluded file '{file_name}'.")
                    continue

                # Process the file
                logging.info(f"Processing file: {source_file}")
                if output_dir:
                    analyze_and_save(source_file, output_dir)

    except Exception as e:
        logging.error(f"Error processing files: {e}")

def main():
    # Retrieve source directory and output directory from environment variables or set default values
    source_directory = os.getenv('SOURCE_DIRECTORY', 'C:/path/to/source')
    output_directory = os.getenv('OUTPUT_DIRECTORY', 'C:/path/to/output')

    logging.info(f"Source directory: {source_directory}")
    logging.info(f"Output directory: {output_directory}")

    # Optional: Define files to exclude
    exclude_files = []  # List of files to exclude, or leave empty to process all files

    # Run the file processing function
    process_files(source_directory, exclude_files, output_directory)

if __name__ == "__main__":
    main()