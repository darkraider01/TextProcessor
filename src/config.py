import os

def configure_environment():
    """Configure environment variables for the project."""
    env_vars = {
        'FILE_DIRECTORY': os.getenv('FILE_DIRECTORY', 'C:/path/to/default/directory'),
        'OUTPUT_DIRECTORY': os.getenv('OUTPUT_DIRECTORY', 'C:/path/to/output/directory'),
    }

    return env_vars

def get_processed_files_log_path(output_directory):
    """Get the path for the processed files log stored in the output directory."""
    return os.path.join(output_directory, 'processed_files.json')
