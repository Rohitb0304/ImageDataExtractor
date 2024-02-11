import csv
from PIL import Image
import pytesseract
import re

def extract_prn_and_name(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)

        # Define a regular expression pattern for PRN and Student's Name
        prn_pattern = re.compile(r'PRN\s+2\s+(\d{12})')
        name_pattern = re.compile(r"STUDENT'S NAME\s*:\s*(.+)")

        # Extract PRN and Student's Name
        prn_match = prn_pattern.search(text)
        name_match = name_pattern.search(text)

        prn = prn_match.group(1) if prn_match else ''
        name = name_match.group(1) if name_match else ''

        return {'PRN': prn, "STUDENT'S NAME": name}

    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

def extract_subject_data(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)

        # Remove unwanted text
        text = re.sub(r'\bCONTROLLER OF EXAMINATIONS\b.*', '', text)

        # Print the extracted text for debugging
        print("Extracted Text:")
        print(text)

        # Define a regular expression pattern for subject information
        pattern = re.compile(r'(ENGINEERING MATHEMATICS(?:\s*-\s*\|)?)\s+(\d+)\s*(\w{1,3})\s*(\w{1,3})')

        subject_data = {}
        matches = pattern.findall(text)

        # Print the pattern matches for debugging
        print("Pattern Matches:")
        print(matches)

        for match in matches:
            subject_name, _, credits, grade = match
            subject_data[subject_name.strip()] = {'Credits': credits, 'Grade': grade}

        return subject_data

    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

def save_data_to_csv(output_path, prn_and_name, subject_data, headers):
    with open(output_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write header
        writer.writerow(headers)

        # Write PRN and Student's Name
        prn_row = [prn_and_name.get(header, '') for header in headers[:2]]
        subjects_row = [subject_data.get(header, {}).get('Credits', '') for header in headers[2:]]
        writer.writerow(prn_row + subjects_row)

        # Write subjects data in the same row with credits at the grades place
        # writer.writerow(subjects_row)

# Replace 'your_image_file.png' with the actual path to your image file
image_file_path = 'uploads/marksheet.png'

# Extract PRN and Student's Name
prn_and_name = extract_prn_and_name(image_file_path)

# Extract subject data using regular expressions
subject_data = extract_subject_data(image_file_path)
 
# Specify the desired headers
custom_headers = ['PRN', "STUDENT'S NAME", 'ENGINEERING MATHEMATICS', 'ENGINEERING CHEMISTRY', 'ENGINEERING MECHANICS', 'COMPUTER PROGRAMMING IN C', 'WORKSHOP PRACTICES', 'Basic Electrical and Electronics Engineering']

# Print extracted data for debugging
print("PRN and Name:", prn_and_name)
print("Subjects Data:", subject_data)

# Save data to CSV with custom headers
save_data_to_csv('output_data/rohit.csv', prn_and_name, subject_data, custom_headers)