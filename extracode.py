import pytesseract
from PIL import Image
import os

# Set up your folder with images (use raw string for Windows paths)
image_folder = r"d:\Python\Python\party\images"

# Tesseract OCR path (adjust this path if necessary)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust path if needed

# Data store
data = []

# Loop through image files
for filename in os.listdir(image_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        filepath = os.path.join(image_folder, filename)

        try:
            # Open image
            image = Image.open(filepath)
            image = image.convert("L")  # Convert to grayscale for better OCR accuracy

            text = pytesseract.image_to_string(image)

            gc_number = None
            gc_type = "UNKNOWN"
            tray_number = None  # Tray number will be determined based on GC_Type

            # Extract GC number (looking for a number that starts with '1' or '9' and is at least 10 digits long)
            for line in text.splitlines():
                if line.strip().isdigit() and (line.startswith("1") or line.startswith("9")) and len(line.strip()) >= 10:
                    gc_number = line.strip()

            # Classify the GC type based on keywords
            if "TO PAY GODOWN" in text.upper() or "TOPAY" in text.upper() or "TO PAY" in text.upper():
                gc_type = "TOPAY"
                tray_number = 1  # Assign tray 1 for "TOPAY"
            elif "PAID GODOWN" in text.upper() or "PAID" in text.upper() or "PAID" in text.lower():
                gc_type = "PAID"
                tray_number = 9  # Assign tray 9 for "PAID"

            # Add data to the list if GC number and type are found
            if gc_number and tray_number is not None:
                data.append({
                    "Filename": filename,
                    "GC_Number": gc_number,
                    "GC_Type": gc_type,
                    "Tray_Number": tray_number  # Store tray number
                })

        except Exception as e:
            data.append({
                "Filename": filename,
                "GC_Number": "Error",
                "GC_Type": f"Error: {str(e)}",
                "Tray_Number": None
            })

# Sort the data by tray number: "1" (TOPAY) first, then "9" (PAID)
sorted_data = sorted(data, key=lambda x: x['Tray_Number'])

# Print sorted data directly
print("\nSorted Data (Tray 1 and 9):")
for entry in sorted_data:
    print(f"Filename: {entry['Filename']} | GC_Number: {entry['GC_Number']} | GC_Type: {entry['GC_Type']} | Tray Number: {entry['Tray_Number']}")

    