import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import re
from PIL import Image

import json
import re
import pytesseract
from pytesseract import image_to_string
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPULAR_PATH = r'C:\poppler-24.08.0\Library\bin'


def extract(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)


# def extract(image):
#     document_text = image_to_string(filepath)
#     return document_text


def parse_lab_tests(text: str):
    lines = text.split('\n')
    data = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Basic heuristic: look for lines that contain 3+ space-separated tokens and a reference range
        match = re.match(
            r"(.+?)\s+([\d.]+)\s*([^\s]*)\s+(\d+\.?\d*)\s*-\s*(\d+\.?\d*)", line)
        if match:
            test_name = match.group(1).strip()
            test_value = match.group(2).strip()
            test_unit = match.group(3).strip()
            ref_min = float(match.group(4))
            ref_max = float(match.group(5))

            try:
                test_value_float = float(test_value)
                out_of_range = not (ref_min <= test_value_float <= ref_max)
            except ValueError:
                out_of_range = None

            data.append({
                "test_name": test_name,
                "test_value": test_value,
                "bio_reference_range": f"{ref_min}-{ref_max}",
                "test_unit": test_unit,
                "lab_test_out_of_range": out_of_range
            })

    return data


def preprocess_image(image: Image.Image) -> Image.Image:
    # Convert PIL to OpenCV
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 3)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    # Convert back to PIL
    return Image.fromarray(thresh)


# filepath = r"C:\Users\AMSHU\Downloads\Medical-Data-Extraction-main\BLR-0425-PA-0041660_KAUSHAL REPORTS_26-04-2025_1047-39_PM@F.pdf_page_9.png"
# image = Image.open(io.BytesIO(await file.read()))
# image = Image.open(filepath)
# image = preprocess_image(image)
# extracted_text = extract(image)

# parsed = parse_lab_tests(extracted_text)

# print(parsed)
