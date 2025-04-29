import tempfile
import shutil
from pathlib import Path
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io

from extractor_2 import extract
from extractor_2 import parse_lab_tests

app = FastAPI()


@app.post("/get-lab-tests")
async def get_lab_tests(file: UploadFile = File(...)):
    try:
        # Save uploaded file to a temporary file
        suffix = Path(file.filename).suffix or ".png"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        # Pass file path to extract()
        extracted_text = extract(tmp_path)
        print("Extracted Text:\n", extracted_text)

        lab_data = parse_lab_tests(extracted_text)

        return JSONResponse(content={
            "is_success": True,
            "data": lab_data
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "is_success": False,
            "error": str(e)
        })


# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# from typing import List
# from PIL import Image
# import pytesseract
# import io
# import re


# import tempfile
# import shutil
# from pathlib import Path

# from extractor_2 import extract
# from extractor_2 import parse_lab_tests


# app = FastAPI()


# def parse_lab_tests(text: str):
#     pattern = re.compile(
#         r'"test_name":\s*"([^"]+)",\s*'
#         r'"test_value":\s*"([^"]+)",\s*'
#         r'"bio_reference_range":\s*"([^"]+)",\s*'
#         r'"test_unit":\s*"([^"]+)",?'
#     )

#     matches = pattern.findall(text)
#     data = []

#     for match in matches:
#         name, value, ref_range, unit = match
#         try:
#             test_value = float(value)
#             ref_min, ref_max = map(float, ref_range.split('-'))
#             out_of_range = not (ref_min <= test_value <= ref_max)
#         except Exception:
#             out_of_range = None  # Unable to determine

#         data.append({
#             "test_name": name,
#             "test_value": value,
#             "bio_reference_range": ref_range,
#             "test_unit": unit,
#             "lab_test_out_of_range": out_of_range
#         })

#     return data


# @app.post("/get-lab-tests2")
# async def get_lab_tests(file: UploadFile = File(...)):
#     try:
#         # Save the uploaded file to a temporary location
#         with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
#             shutil.copyfileobj(file.file, tmp)
#             tmp_path = tmp.name

#         # Now you have the filepath
#         print("Temporary file path:", tmp_path)

#         # Open image from file path if needed
#         # image = Image.open(tmp_path)
#         # image = preprocess_image(image)
#         extracted_text = extract(tmp_path)

#         lab_data = parse_lab_tests(extracted_text)

#         image = Image.open(io.BytesIO(await file.read()))
#         extracted_text = extract(image)
#         print(extracted_text)
#         # extracted_text = pytesseract.image_to_string(image)
#         lab_data = parse_lab_tests(extracted_text)

#         return JSONResponse(content={
#             "is_success": True,
#             "data": lab_data
#         })
#     except Exception as e:
#         return JSONResponse(status_code=500, content={
#             "is_success": False,
#             "error": str(e)
#         })


# @app.post("/get-lab-tests")
# async def get_lab_tests(file: UploadFile = File(...)):
#     try:
#         image = Image.open(io.BytesIO(await file.read()))
#         extracted_text = extract(image)
#         print(extracted_text)
#         # extracted_text = pytesseract.image_to_string(image)
#         lab_data = parse_lab_tests(extracted_text)

#         return JSONResponse(content={
#             "is_success": True,
#             "data": lab_data
#         })
#     except Exception as e:
#         return JSONResponse(status_code=500, content={
#             "is_success": False,
#             "error": str(e)
#         })
