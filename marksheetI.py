import csv
import pytesseract
from PIL import Image
import re
import os

class MarksheetI:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_data_to_csv(self, data, headers):
        with open(self.file_path, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Write headers if the file is empty
            if os.path.getsize(self.file_path) == 0:
                writer.writerow(headers)
            writer.writerows(data)

    def extract_prn_and_name(self):
        try:
            img = Image.open(self.image_path)
            text = pytesseract.image_to_string(img)
            prn_pattern = re.compile(r'PRN\s+2\s+(\d{13})')
            name_pattern = re.compile(r"STUDENT'S NAME\s*:\s*(.+)")

            prn_match = prn_pattern.search(text)
            name_match = name_pattern.search(text)

            prn = prn_match.group(1) if prn_match else ''
            name = name_match.group(1) if name_match else ''

            return {'PRN': prn, "STUDENT'S NAME": name}
        except Exception as e:
            print(f"Error: {e}")
            return {}

    def extract_subject_data(self):
        try:
            img = Image.open(self.image_path)
            text = pytesseract.image_to_string(img)
            text = re.sub(r'\bCONTROLLER OF EXAMINATIONS\b.*', '', text)
            pattern = re.compile(r'(ENGINEERING MATHEMATICS(?:\s*-\s*\|)?|ENGINEERING CHEMISTRY|ENGINEERING MECHANICS|COMPUTER PROGRAMMING IN C|WORKSHOP PRACTICES|Basic Electrical and Electronics Engineering)\s+(\d+|[A-Za-z]{2})\s*([A-Za-z]{1,2})([A-Za-z]{1,2})')

            subject_data = {}
            matches = pattern.findall(text)

            for match in matches:
                subject_name, credits, grade1, grade2 = match
                grade = grade1 + grade2
                subject_name = subject_name.strip().upper().replace('-', '').replace('|', '').strip()
                subject_data[subject_name] = {'Credits': credits, 'Grade': grade}

            if 'BASIC ELECTRICAL AND ELECTRONICS ENGINEERING' not in subject_data:
                subject_data['BASIC ELECTRICAL AND ELECTRONICS ENGINEERING'] = {'Credits': '', 'Grade': ''}

            return subject_data
        except Exception as e:
            print(f"Error: {e}")
            return {}

    def locate_cgpa_sgpa(self, cgpa_coords, sgpa_coords):
        try:
            img = Image.open(self.image_path)
            cgpa_text = pytesseract.image_to_string(img.crop(cgpa_coords))
            sgpa_text = pytesseract.image_to_string(img.crop(sgpa_coords))
            cgpa = cgpa_text.strip() if cgpa_text else None
            sgpa = sgpa_text.strip() if sgpa_text else None
            return {'CGPA': cgpa, 'SGPA': sgpa}
        except Exception as e:
            print(f"Error locating CGPA and SGPA: {e}")
            return {'CGPA': None, 'SGPA': None}

    def save_data_to_csv(self, output_path, headers):
        prn_and_name = self.extract_prn_and_name()
        subject_data = self.extract_subject_data()
        cgpa_sgpa = self.locate_cgpa_sgpa((1173, 1594, 1243, 1620), (549, 1595, 618, 1624))

        with open(output_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)
            prn_row = [prn_and_name.get(header, '') for header in headers[:2]]
            subjects_row = [subject_data.get(header, {}).get('Grade', '') for header in headers[2:8]]
            sgpa_cgpa_row = [cgpa_sgpa.get('SGPA', ''), cgpa_sgpa.get('CGPA', '')]
            writer.writerow(prn_row + subjects_row + sgpa_cgpa_row)
