from PIL import Image
import pytesseract

def extract_text_from_image(image_path):
    try:
        # Open the image file
        img = Image.open(image_path)

        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(img)

        return text.strip()  # Strip leading and trailing whitespaces

    except Exception as e:
        return f"Error: {e}"

# Replace 'your_image_file.png' with the actual path to your image file
image_file_path = 'uploads/marksheet-II.png'

# Extract text from the image
extracted_text = extract_text_from_image(image_file_path)

# Print the extracted text
print(extracted_text)