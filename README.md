## Text Analysis and Extraction Tool

## Overview

This is a comprehensive text analysis tool that processes various file types, including images, JSON, and text files. It extracts and analyzes text data to generate detailed analysis results. The project also includes functionality for generating a requirements file to capture the environment details.

## Features

### TextAnalyzer

- **Initialization**:
  - `__init__()`: Initializes the `TextAnalyzer` with models for NLP tasks.

- **Text Processing**:
  - `load_text(text)`: Loads text for processing.
  - `sentence_splitting()`: Splits text into sentences.
  - `word_tokenization()`: Tokenizes text into words.
  - `pos_tagging()`: Tags parts of speech in the text.
  - `bigram_analysis()`: Analyzes bigrams in the text.
  - `trigram_analysis()`: Analyzes trigrams in the text.
  - `collocations()`: Identifies word collocations.
  - `concordance(word)`: Finds occurrences of a word within its context.

- **Sentiment Analysis**:
  - `sentiment_analysis()`: Analyzes the sentiment of the text.

- **Language Detection**:
  - `language_detection()`: Detects the language of the text.

### TextExtractor 

- **Initialization**:
  - `__init__(tesseract_path=None)`: Initializes the `TextExtractor` with an optional path to the Tesseract OCR executable.

- **Image Resizing**:
  - `_resize_image(img, max_size=800)`: Resizes the image while maintaining the aspect ratio to a maximum size of 800 pixels for better processing.

- **Image Preprocessing**:
  - `_preprocess_image(img)`: Converts the image to grayscale, applies Gaussian blur, adaptive thresholding, and morphological operations to enhance text regions.

- **Contour Detection**:
  - `_find_contours(thresh)`: Finds and filters contours in the thresholded image to identify potential text areas.

- **Text Area Extraction**:
  - `_extract_text_area(img, x, y, w, h)`: Extracts text from a specified rectangular area in the image by saving the region as a temporary file and applying OCR.

- **Image Processing and Text Extraction**:
  - `process_image(file_path)`: Processes the given image file to detect text areas, extracts text from those areas, and displays the image with detected regions highlighted. Shows extracted text in the console.

### Key Features:

- **Tesseract Integration**: Supports the use of Tesseract OCR for text extraction, with an option to specify the Tesseract executable path.
- **Image Resizing**: Adjusts image size for optimal processing while preserving aspect ratio.
- **Advanced Preprocessing**: Uses techniques like grayscale conversion, blurring, thresholding, and morphological operations to enhance text detection.
- **Contour-Based Text Detection**: Identifies and processes regions of interest in the image based on contours.
- **Text Extraction**: Extracts text from detected areas and prints it to the console.
- **Visualization**: Displays the image with detected text regions highlighted for visual verification.

## Installation

### Prerequisites

- Python 3.12 or later
- [Other dependencies or tools]

### Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/username/repository.git
   ```
2. Navigate to the project directory:
   ```sh
   cd repository
   ```
3. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```
5. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

To use this tool, follow these steps:

1. Set environment variables for your directories:
   - `FILE_DIRECTORY`: Path to the directory containing the files to be processed.
   - `OUTPUT_DIRECTORY`: Path to the directory where results will be saved.
   - `PROCESSED_FILES_LOG`: Path to the JSON log file for processed files.

2. Run the main script:
   ```sh
   python src/main.py
   ```

### Example Command

For Windows:
```sh
setx FILE_DIRECTORY C:\path\to\files
setx OUTPUT_DIRECTORY C:\path\to\output
setx PROCESSED_FILES_LOG C:\path\to\processed_files.json
python src/main.py
```

For macOS/Linux:
```sh
export FILE_DIRECTORY=/path/to/files
export OUTPUT_DIRECTORY=/path/to/output
export PROCESSED_FILES_LOG=/path/to/processed_files.json
python src/main.py
```
```

You can copy and paste this directly into your `README.md` file. Let me know if you need any more changes!
