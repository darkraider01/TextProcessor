import os
import datetime
import uuid
import logging
import subprocess

from src.file_processor import analyze_and_save

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve directory paths from environment variables
file_directory = os.getenv('FILE_DIRECTORY', 'C:/path/to/default/directory')  # Default if not provided
output_directory = os.getenv('OUTPUT_DIRECTORY', 'C:/path/to/output/directory')  # Default if not provided
processed_files_log = os.getenv('PROCESSED_FILES_LOG', 'processed_files.json')  # Log file for processed files

def generate_requirements_file(output_dir):
    """
    Generate a requirements.txt file listing all installed packages.
    - Uses pip freeze to get the list of installed packages and versions.
    - Saves this list to a requirements.txt file in the specified output directory.
    """
    try:
        requirements_file = os.path.join(output_dir, 'requirements.txt')
        with open(requirements_file, 'w') as file:
            subprocess.run(['pip', 'freeze'], stdout=file, check=True)
        logging.info(f"Requirements file created at: {requirements_file}")
    except Exception as e:
        logging.error(f"Error generating requirements file: {e}")

def main():
    # Log retrieved paths
    logging.info(f"File directory: {file_directory}")
    logging.info(f"Output directory: {output_directory}")
    logging.info(f"Processed files log: {processed_files_log}")

    if not os.path.exists(file_directory):
        logging.error(f"Directory '{file_directory}' does not exist.")
        return

    # Generate a unique folder name for this run
    now = datetime.datetime.now()
    timestamp = now.strftime("%d-%m-%Y_%H-%M")
    unique_run_folder = f"run_{timestamp}_{uuid.uuid4().hex}"
    unique_output_dir = os.path.join(output_directory, unique_run_folder)

    # Create the unique run directory
    os.makedirs(unique_output_dir, exist_ok=True)
    logging.info(f"Results will be saved in folder: {unique_output_dir}")

    # Generate the requirements file
    generate_requirements_file(unique_output_dir)

    # Process files in the source directory and its subdirectories
    for root, dirs, files in os.walk(file_directory):
        logging.info(f"Scanning directory: {root}")
        for file_name in files:
            source_file = os.path.join(root, file_name)

            # Log the file being processed
            logging.info(f"Processing file: {source_file}")
            try:
                analyze_and_save(source_file, unique_output_dir, processed_files_log)
            except Exception as e:
                logging.error(f"Error processing file {source_file}: {e}")

if __name__ == "__main__":
    main()
