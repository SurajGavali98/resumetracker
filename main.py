from fastapi import FastAPI, UploadFile, File
import shutil
import os
import ollama

from utils.parser import extract_text_from_pdf, extract_text_from_docx

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Resume AI Parser running"}


@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    if file.filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file_path)

    elif file.filename.endswith(".docx"):
        resume_text = extract_text_from_docx(file_path)

    else:
        return {"error": "Unsupported file format"}

    prompt = f"""
   Extract skills and years of experience from this resume. Return JSON only.
    Resume:
    {resume_text}
    """

    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return {
        "parsed_data": response["message"]["content"]
    }