import pytesseract
from PIL import Image
import os

# Set up your folder with images (use raw string for Windows paths)
image_folder = r"d:\Python\Python\party\images"

# Tesseract OCR path (adjust this path if necessary)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Data store
data = []

# Loop through image files
for filename in os.listdir(image_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        filepath = os.path.join(image_folder, filename)
        print(f"Processing: {filename}")
        try:
            # Open image
            image = Image.open(filepath)
            image = image.convert("L")  # Convert to grayscale for better OCR accuracy
            print(f"Extracting text from: {filename}")
            text = pytesseract.image_to_string(image)

            lr_number = None
            tray_number = None

            # Extract LR number (number starting with '1' or '9' and at least 10 digits)
            for line in text.splitlines():
                clean_line = line.strip()
                if clean_line.isdigit() and (clean_line.startswith("1") or clean_line.startswith("9")) and len(clean_line) >= 10:
                    lr_number = clean_line
                    break  # Stop after finding the first valid LR number

            # Determine tray number based on last digit
            if lr_number:
                last_digit = lr_number[-1]
                if last_digit.isdigit():
                    tray_number = int(last_digit)  # Tray 0 to 9

            # Append the information to data
            if lr_number and tray_number is not None:
                data.append({
                    "Filename": filename,
                    "LR_Number": lr_number,
                    "Tray_Number": tray_number
                })

        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            data.append({
                "Filename": filename,
                "LR_Number": "Error",
                "Tray_Number": None
            })

# Sort the data by Tray Number (0–9)
sorted_data = sorted(data, key=lambda x: x['Tray_Number'] if x['Tray_Number'] is not None else 99)

# Print sorted data
print("\nSorted Data by Tray Number (0-9):")
for entry in sorted_data:
    print(f"Filename: {entry['Filename']} | LR_Number: {entry['LR_Number']} | Tray Number: {entry['Tray_Number']}")