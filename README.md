RUN app.py using this in terminal:

uvicorn app:app --reload

use your endpoint by this:

curl -X POST -F "file=@C:\Users\AMSHU\Downloads\Medical-Data-Extraction-main\BLR-0425-PA-0041660_KAUSHAL REPORTS_26-04-2025_1047-39_PM@F.pdf_page_9.png" http://127.0.0.1:8000/get-lab-tests

ENDPOINT URL:

http://127.0.0.1:8000/get-lab-tests
