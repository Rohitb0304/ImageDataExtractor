import csv
import pytesseract
from PIL import Image
import re

class MarksheetI:
    def __init__(self, image_path):
        self.image_path = image_path
def extract_prn_and_name(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)

        # Define a regular expression pattern for PRN and Student's Name
        prn_pattern = re.compile(r'PRN\s+2\s+(\d{13})')
        name_pattern = re.compile(r"STUDENT'S NAME\s*:\s*(.+)")

        print("Extracted Text:")
        print(text)
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

        # Define a regular expression pattern for subject information
        pattern = re.compile(r'(ENGINEERING MATHEMATICS(?:\s*-\s*\|)?|ENGINEERING CHEMISTRY|ENGINEERING MECHANICS|COMPUTER PROGRAMMING IN C|WORKSHOP PRACTICES|Basic Electrical and Electronics Engineering)\s+(\d+|[A-Za-z]{2})\s*([A-Za-z]{1,2})([A-Za-z]{1,2})')

        subject_data = {}
        matches = pattern.findall(text)

        for match in matches:
            subject_name, credits, grade1, grade2 = match
            # Concatenate the two alphabet characters for the grade
            grade = grade1 + grade2
            # Normalize subject name for easier matching
            subject_name = subject_name.strip().upper().replace('-', '').replace('|', '').strip()
            subject_data[subject_name] = {'Credits': credits, 'Grade': grade}

        # If the grade for Basic Electrical and Electronics Engineering is not found, set it to an empty string
        if 'BASIC ELECTRICAL AND ELECTRONICS ENGINEERING' not in subject_data:
            subject_data['BASIC ELECTRICAL AND ELECTRONICS ENGINEERING'] = {'Credits': '', 'Grade': ''}

        return subject_data

    except Exception as e:
        print(f"Error: {e}")
        return {}

def locate_cgpa_sgpa(image_path, cgpa_coords, sgpa_coords):
    try:
        # Process the image using OCR to extract text
        img = Image.open(image_path)

        # Extract CGPA and SGPA using provided coordinates
        cgpa_text = pytesseract.image_to_string(img.crop(cgpa_coords))
        sgpa_text = pytesseract.image_to_string(img.crop(sgpa_coords))

        # Extracted CGPA and SGPA
        cgpa = cgpa_text.strip() if cgpa_text else None
        sgpa = sgpa_text.strip() if sgpa_text else None

        return {'CGPA': cgpa, 'SGPA': sgpa}

    except Exception as e:
        print(f"Error locating CGPA and SGPA: {e}")
        return {'CGPA': None, 'SGPA': None}


# Testing Functions
def save_data_to_csv(output_path, prn_and_name, subject_data, cgpa_sgpa, headers):
    with open(output_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write header
        writer.writerow(headers)

        # Write PRN and Student's Name
        prn_row = [prn_and_name.get(header, '') for header in headers[:2]]

        # Write subject grades
        subjects_row = [subject_data.get(header, {}).get('Grade', '') for header in headers[2:8]]

        # Write SGPA and CGPA
        sgpa_cgpa_row = [cgpa_sgpa.get('SGPA', ''), cgpa_sgpa.get('CGPA', '')]

        writer.writerow(prn_row + subjects_row + sgpa_cgpa_row)


# Replace 'your_image_file.png' with the actual path to your image file
image_file_path = 'uploads/marksheet.png'

# Extract PRN and Student's Name
prn_and_name = extract_prn_and_name(image_file_path)

# Extract subject data using regular expressions
subject_data = extract_subject_data(image_file_path)

# Define coordinates for CGPA and SGPA
cgpa_coords = (1173, 1594, 1243, 1620)
sgpa_coords = (549, 1595, 618, 1624)

# Locate CGPA and SGPA
cgpa_sgpa = locate_cgpa_sgpa(image_file_path, cgpa_coords, sgpa_coords)

 
# Specify the desired headers
custom_headers = ['PRN', "STUDENT'S NAME", "ENGINEERING MATHEMATICS", 'ENGINEERING CHEMISTRY', 'ENGINEERING MECHANICS', 'COMPUTER PROGRAMMING IN C', 'WORKSHOP PRACTICES', 'Basic Electrical and Electronics Engineering', 'SGPA', 'CGPA']

# Save data to CSV with custom headers
save_data_to_csv('output_data/marksheet-I.csv', prn_and_name, subject_data, cgpa_sgpa, custom_headers)

# Print extracted data for debugging
print("PRN and Name:", prn_and_name)
print("Subjects Data:", subject_data)
print("CGPA and SGPA:", cgpa_sgpa)







# import csv
# from PIL import Image
# import pytesseract
# import re

# def extract_prn_and_name(image_path):
#     try:
#         img = Image.open(image_path)
#         text = pytesseract.image_to_string(img)

#         # Define a regular expression pattern for PRN and Student's Name
#         prn_pattern = re.compile(r'PRN\s+2\s+(\d{13})')
#         name_pattern = re.compile(r"STUDENT'S NAME\s*:\s*(.+)")

#         print("Extracted Text:")
#         print(text)
#         # Extract PRN and Student's Name
#         prn_match = prn_pattern.search(text)
#         name_match = name_pattern.search(text)

#         prn = prn_match.group(1) if prn_match else ''
#         name = name_match.group(1) if name_match else ''

#         return {'PRN': prn, "STUDENT'S NAME": name}
    

#     except Exception as e:
#         print(f"Error: {e}")
#         return f"Error: {e}"


# def extract_subject_data(image_path):
#     try:
#         img = Image.open(image_path)
#         text = pytesseract.image_to_string(img)

#         # Remove unwanted text
#         text = re.sub(r'\bCONTROLLER OF EXAMINATIONS\b.*', '', text)

#         # Define a regular expression pattern for subject information
#         pattern = re.compile(r'(ENGINEERING MATHEMATICS(?:\s*-\s*\|)?|ENGINEERING CHEMISTRY|ENGINEERING MECHANICS|COMPUTER PROGRAMMING IN C|WORKSHOP PRACTICES|Basic Electrical and Electronics Engineering)\s+(\d+)\s*([A-Za-z]{1,2})([A-Za-z]{1,2})')

#         subject_data = {}
#         matches = pattern.findall(text)

#         for match in matches:
#             subject_name, credits, grade1, grade2 = match
#             # Concatenate the two alphabet characters for the grade
#             grade = grade1 + grade2
#             # Ensure that credits are assigned correctly
#             if credits.isdigit():
#                 credits = int(credits)
#             # Normalize subject name for easier matching
#             subject_name = subject_name.strip().upper().replace('-', '').replace('|', '').strip()
#             subject_data[subject_name] = {'Credits': credits, 'Grade': grade}

#         return subject_data

#     except Exception as e:
#         print(f"Error: {e}")
#         return {}

# # Testing Functions
# def save_data_to_csv(output_path, prn_and_name, subject_data, headers):
#     with open(output_path, 'w', newline='') as csv_file:
#         writer = csv.writer(csv_file)

#         # Write header
#         writer.writerow(headers)

#         # Write PRN and Student's Name
#         prn_row = [prn_and_name.get(header, '') for header in headers[:2]]

#         # Write subject grades
#         subjects_row = [subject_data.get(header, {}).get('Grade', '') for header in headers[2:]]
#         writer.writerow(prn_row + subjects_row)


# # Replace 'your_image_file.png' with the actual path to your image file
# image_file_path = 'uploads/marksheet.png'

# # Extract PRN and Student's Name
# prn_and_name = extract_prn_and_name(image_file_path)

# # Extract subject data using regular expressions
# subject_data = extract_subject_data(image_file_path)
 
# # Specify the desired headers
# custom_headers = ['PRN', "STUDENT'S NAME", "ENGINEERING MATHEMATICS", 'ENGINEERING CHEMISTRY', 'ENGINEERING MECHANICS', 'COMPUTER PROGRAMMING IN C', 'WORKSHOP PRACTICES', 'Basic Electrical and Electronics Engineering']

# # Save data to CSV with custom headers
# save_data_to_csv('output_data/marksheet-I.csv', prn_and_name, subject_data, custom_headers)

# # Print extracted data for debugging
# print("PRN and Name:", prn_and_name)
# print("Subjects Data:", subject_data)
