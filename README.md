### Problem Statement:

Develop a scalable and accurate solution to process lab reports with the objective of extracting all lab test
names, their corresponding values, and reference ranges. Use the provided dataset of lab report images to
build logic/model.
The logic must be implemented in Python and deployed as a Fast API service. The API should expose a
POST endpoint /get-lab-tests that accepts an image file as input and returns the extracted lab test data in a
structured JSON format.

### Dataset link:

https://drive.google.com/file/d/1LzG7oJ-cqGHK9KbwXnWfkWgnQ3xi8Cr9/view?usp=sharing

## SOLUTION:

#### RUN app.py using this in terminal:

uvicorn app:app --reload

#### use your endpoint by this:

curl -X POST -F "file=@C:\Users\AMSHU\Downloads\Medical-Data-Extraction-main\BLR-0425-PA-0041660_KAUSHAL REPORTS_26-04-2025_1047-39_PM@F.pdf_page_9.png" http://127.0.0.1:8000/get-lab-tests

#### ENDPOINT URL:

http://127.0.0.1:8000/get-lab-tests
