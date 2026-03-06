from fastapi import FastAPI, UploadFile, File
import shutil
import os
from dotenv import load_dotenv
from openai import OpenAI

from utils.resume_parser import extract_text_from_pdf, extract_text_from_docx

load_dotenv()

client = OpenAI()

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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
    Extract the following information from this resume:

    1. Skills
    2. Years of experience
    3. Technologies used
    4. Previous job roles

    Return JSON format.

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert resume parser."},
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content

    return {
        "parsed_data": result
    }