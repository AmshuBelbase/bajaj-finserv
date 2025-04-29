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
