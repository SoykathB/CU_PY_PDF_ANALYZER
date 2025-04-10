from fastapi import FastAPI, File, UploadFile, Form
import os
from fastapi.responses import JSONResponse
from docling.document_converter import DocumentConverter
import pymupdf
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
from pdf_extractor.src.pdf_extractor.data_extract_crew import PDFEXTRACTOR
app = FastAPI()
import requests
@app.post("/getPDFDATA")
async def getPDFDATA(file: UploadFile = File(...),data: str = Form(...)):
    file_bytes = await file.read()
    url = "Your URL"
    files = {
        'file': (file.filename, file_bytes, file.content_type)
    }
    response = requests.post(url, files=files)
    if(response.text):
        output = json.loads(response.text)
    else:
        raise Exception('Failed to process document')

    crewObject = PDFEXTRACTOR()
    inputs = {
        'configuration': data,
        'pdf_data': output.get('data')
    }
    final_answer = crewObject.kickoff(inputs=inputs)
    final_answer.raw
    data = extract_json_like_substring(final_answer.raw)
    cleaned_json_string = data.replace("\n", "")
    output_data = json.loads(cleaned_json_string)
    return {'data': output_data}

def extract_json_like_substring(s):
    first_index = min((s.find('['), s.find('{')), key=lambda x: x if x != -1 else float('inf'))
    last_index = max(s.rfind(']'), s.rfind('}'))

    if first_index == -1 or last_index == -1 or first_index > last_index:
        return None  # No valid JSON-like structure found

    return s[first_index:last_index+1]
    