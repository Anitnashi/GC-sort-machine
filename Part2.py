import pytesseract
from PIL import Image
import csv
import re

# Manually set the Tesseract path if not using system PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load party data from the CSV file
party_map = {}
try:
    with open('d:/Python/Python/party/party_codes.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            code = row['PartyCode'].strip()
            category = row['Category'].strip()
            party_map[code] = category
    print("Party data loaded successfully.")
except FileNotFoundError:
    print("Error: The file 'party_codes.csv' was not found.")
    exit()

# Process image to extract codes and group by category
def process_image(file_path):
    try:
        text = pytesseract.image_to_string(Image.open(file_path))
    except Exception as e:
        print(f"Error processing the image: {e}")
        return

    codes_found = re.findall(r'\b\d{5,6}\b', text)  # Match both 5 and 6-digit codes
    unique_codes = sorted(set(codes_found))

    tray1 = []  # To-Pay
    tray2 = []  # Paid
    tray3 = []  # Others / Advance

    for code in unique_codes:
        if code in party_map:
            category = party_map[code]
            if category == 'To-Pay':
                tray1.append(code)
            elif category == 'Paid':
                tray2.append(code)
            else:
                tray3.append(code)

    # Display sorted by category
    if tray1:
        print("\nTray 1 - To-Pay:")
        for code in tray1:
            print(code)
    if tray2:
        print("\nTray 2 - Paid:")
        for code in tray2:
            print(code)
    if tray3:
        print("\nTray 3 - Advance/Others:")
        for code in tray3:
            print(code)
    if not tray1 and not tray2 and not tray3:
        print("No valid party codes found in the image.")

# Run the function
image_path = 'd:/Python/Python/party/scanned_cr_image.png'
process_image(image_path)