import json
import re
import pytesseract
from pytesseract import image_to_string
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPULAR_PATH = r'C:\poppler-24.08.0\Library\bin'


def extract_value(line):
    parts = line.split()
    try:
        # Look for float values first
        for i, part in enumerate(parts):
            if re.match(r"\d+(\.\d+)?", part):
                return part, " ".join(parts[i+1:])
    except:
        pass
    return None, None


def parse_lab_report(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    data = {
        "patient_name": None,
        "reference_doctor": None,
        "hospital": None,
        "uhid": None,
        "tests": []
    }

    current_category = None
    current_test_list = []

    for line in lines:
        if "Reference:" in line:
            data["patient_name"], data["reference_doctor"] = line.split(
                "Reference:")
            data["patient_name"] = data["patient_name"].strip()
            data["reference_doctor"] = data["reference_doctor"].strip()

        elif "UHID" in line:
            uhid_match = re.search(r"UHID\s*:\s*(\S+)", line)
            if uhid_match:
                data["uhid"] = uhid_match.group(1)

        elif "HOSPITAL" in line or "Hospital" in line:
            data["hospital"] = "AJ Hospital & Research Centre, Mangalore"

        elif line.startswith("#Blood"):
            if current_category and current_test_list:
                data["tests"].append({
                    "category": current_category,
                    "tests": current_test_list
                })
                current_test_list = []
            current_category = line.replace("#", "").strip()

        elif re.search(r"\d", line) and not line.startswith("PIN"):
            test_name = re.sub(r"\s*\(.*?\)", "", line).strip()
            value, unit = extract_value(line)
            if value:
                current_test_list.append({
                    "name": test_name,
                    "result": value,
                    "unit": unit,
                    "reference_range": None  # You can extract from separate section
                })

    if current_category and current_test_list:
        data["tests"].append({
            "category": current_category,
            "tests": current_test_list
        })

    return data


def extract(filepath):
    document_text = image_to_string(filepath)
    return document_text


if __name__ == "__main__":
    data = extract(
        r"C:\Users\AMSHU\Downloads\Medical-Data-Extraction-main\BLR-0425-PA-0041660_KAUSHAL REPORTS_26-04-2025_1047-39_PM@F.pdf_page_9.png")
    print(data)
