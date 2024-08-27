import os
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_requirements_file(output_dir):
    """
    Generate a requirements.txt file listing all installed packages.
    - Uses pip freeze to get the list of installed packages and versions.
    - Saves this list to a requirements.txt file in the specified output directory.
    """
    try:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        logging.info(f"Created output directory: {output_dir}")

        requirements_file = os.path.join(output_dir, 'requirements.txt')
        with open(requirements_file, 'w') as file:
            subprocess.run(['pip', 'freeze'], stdout=file, check=True)
        logging.info(f"Requirements file created at: {requirements_file}")
    except Exception as e:
        logging.error(f"Error generating requirements file: {e}")

def main():
    # Define the relative path for the requirements directory
    output_directory = os.path.join(os.path.dirname(__file__), 'requirements')  # Creates a 'requirements' folder in the project directory

    # Log the directory where requirements will be saved
    logging.info(f"Output directory for requirements file: {output_directory}")

    # Generate requirements file in the specified directory
    generate_requirements_file(output_directory)

if __name__ == "__main__":
    main()
