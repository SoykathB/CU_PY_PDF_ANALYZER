from fastapi import FastAPI, File, UploadFile
import os
from fastapi.responses import JSONResponse
from docling.document_converter import DocumentConverter
app = FastAPI()

@app.post("/extractDATA")
def upload_file(file: UploadFile = File(...)):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(base_dir, file.filename)
    try:
        with open(file_location, "wb") as f:
            f.write(file.file.read())  # No await here
        converter = DocumentConverter()
        result = converter.convert(file_location)
        if os.path.exists(file_location):
            os.remove(file_location)
        # Optionally, process the result further based on user_query
        return {"data": result.document.export_to_markdown()}
        # return JSONResponse(content={"message": "File uploaded successfully", "filename": file.filename}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
