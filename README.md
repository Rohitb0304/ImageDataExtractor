## ImageDataExtractor

**ImageDataExtractor** simplifies text extraction from images. Effortlessly convert image data to editable text with OCR technology. Perfect for digitizing documents, extracting student info, or capturing details from receipts. Fast, efficient, and user-friendly.

### Installation

#### Python Installation

Ensure you have Python 3 installed on your system. You can download it from the official website: [Python.org](https://www.python.org/downloads/)

#### Libraries Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required libraries.

```bash
pip install pytesseract pillow
```

#### Tesseract Installation

For text extraction, **ImageDataExtractor** utilizes Tesseract OCR. Install Tesseract OCR on your system.

- **Mac** (using Homebrew):

```bash
brew install tesseract
```

- **Windows**:

Download the installer from the [Tesseract GitHub page](https://github.com/tesseract-ocr/tesseract/releases) and follow the installation instructions.

- **Ubuntu**:

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ImageDataExtractor.git
```

2. Navigate to the project directory:

```bash
cd ImageDataExtractor
```

3. Place your image files in the `images` directory.

4. Run the Python script:

```bash
python main.py
```

### Usage

- Modify the `main.py` script to customize text extraction and processing according to your requirements.

- Ensure your image files are clear and properly aligned for accurate text extraction.

- Explore different OCR settings and techniques to improve extraction accuracy.

### License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
