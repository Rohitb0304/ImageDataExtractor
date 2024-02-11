import csv
from PIL import Image
import pytesseract

class MarksheetII:
    def __init__(self, image_path):
        self.image_path = image_path


# Set the path to the Tesseract executable (update this path based on your installation)
# pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# Function to extract text from a specific region
def extract_text_from_region(image_path, region_coordinates):
    img = Image.open(image_path)

    # Ensure the region coordinates are within the image boundaries
    left, top, right, bottom = region_coordinates
    left = max(0, left)
    top = max(0, top)
    right = min(img.width, right)
    bottom = min(img.height, bottom)

    # Crop the image to the specified region
    region_img = img.crop((left, top, right, bottom))

    text = pytesseract.image_to_string(region_img)
    return text.strip()  # Strip leading and trailing whitespaces

# Function to save data to CSV with custom header
def save_data_to_csv(output_path, data_list):
    with open(output_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Ensure the data_list is not empty before writing to CSV
        if data_list:
            writer.writerow(data_list)

# Define the image path
image_path = 'uploads/marksheet-II.png'

# Define coordinates for different regions
prn_coordinates = (485, 541, 683, 573)  # Updated coordinates
student_name_coordinates = (487, 603, 851, 631)
engineering_math_coordinates = [(1324, 740, 1377, 762)]
engineering_physics_coordinates = [(1323, 797, 1377, 820)]
engineering_graphics_coordinates = [(1321, 855, 1375, 877)]  # Updated coordinates
energy_environment_engineering_coordinates = [(1321, 913, 1376, 936)]
basic_civil_mechanical_engineering_coordinates = [(1320, 1064, 1375, 1094)]
seminar_coordinates = [(1325, 1311, 1372, 1342)]


# Extract text from each region
prn_text = extract_text_from_region(image_path, prn_coordinates)
student_name_text = extract_text_from_region(image_path, student_name_coordinates)
engineering_math_text = [extract_text_from_region(image_path, coord) for coord in engineering_math_coordinates]
engineering_physics_text = [extract_text_from_region(image_path, coord) for coord in engineering_physics_coordinates]
engineering_graphics_text = [extract_text_from_region(image_path, coord) for coord in engineering_graphics_coordinates]
energy_environment_engineering_text = [extract_text_from_region(image_path, coord) for coord in energy_environment_engineering_coordinates]
basic_civil_mechanical_engineering_text = [extract_text_from_region(image_path, coord) for coord in basic_civil_mechanical_engineering_coordinates]
seminar_text = [extract_text_from_region(image_path, coord) for coord in seminar_coordinates]

# Save data to CSV with custom header
output_data = [
    prn_text, student_name_text, engineering_math_text[0], engineering_physics_text[0],
    engineering_graphics_text[0], energy_environment_engineering_text[0],
    basic_civil_mechanical_engineering_text[0], seminar_text[0]
]

header = ['PRN', "STUDENT'S NAME", 'Engineering Mathematics-II', 'Engineering Physics',
          'Engineering Graphics', 'Energy and Environment Engineering', 'Basic Civil and Mechanical Engineering',
          'Seminar']

save_data_to_csv('extracts/marksheet-II.csv', header)
save_data_to_csv('extracts/marksheet-II.csv', output_data)
print("data saved to csv file successfully!")
print(output_data)
