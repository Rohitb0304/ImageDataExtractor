import csv
from PIL import Image
import pytesseract
import os

class MarksheetII:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_data_to_csv(self, data, headers):
        with open(self.file_path, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Write headers if the file is empty
            if os.path.getsize(self.file_path) == 0:
                writer.writerow(headers)
            writer.writerows(data)

            
    def extract_text_from_region(self, region_coordinates):
        img = Image.open(self.image_path)
        left, top, right, bottom = region_coordinates
        left = max(0, left)
        top = max(0, top)
        right = min(img.width, right)
        bottom = min(img.height, bottom)
        region_img = img.crop((left, top, right, bottom))
        text = pytesseract.image_to_string(region_img)
        return text.strip()

    def save_data_to_csv(self, output_path, header):
        prn_text = self.extract_text_from_region((485, 541, 683, 573))
        student_name_text = self.extract_text_from_region((487, 603, 851, 631))

        output_data = [
            prn_text, student_name_text,
            self.extract_text_from_region((1324, 740, 1377, 762)),
            self.extract_text_from_region((1323, 797, 1377, 820)),
            self.extract_text_from_region((1321, 855, 1375, 877)),
            self.extract_text_from_region((1321, 913, 1376, 936)),
            self.extract_text_from_region((1320, 1064, 1375, 1094)),
            self.extract_text_from_region((1325, 1311, 1372, 1342))
        ]

        with open(output_path, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            if output_data:
                writer.writerow(output_data)
