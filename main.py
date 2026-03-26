# Line 1
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import os
from pypdf import PdfReader

# Line 6
app = FastAPI()

# Line 9 → Create uploads folder if not exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Line 13 -------------------------------
# 📄 Upload PDF + Extract Text
# -------------------------------
@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    # Line 18 → File path
    file_path = f"uploads/{file.filename}"

    # Line 21 → Save file
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Line 25 → Extract text from PDF
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    # Line 34 → Save extracted text
    with open("extracted.txt", "w", encoding="utf-8") as f:
        f.write(text)

    return {"message": "PDF uploaded and text extracted successfully"}


# Line 41 -------------------------------
# ❓ Ask Question API
# -------------------------------
@app.get("/ask")
def ask_question(query: str):

    # Line 46 → Read extracted text
    with open("extracted.txt", "r", encoding="utf-8") as f:
        text = f.read()

    results = []

    # Line 52 → Search keyword
    for line in text.split("\n"):
        if query.lower() in line.lower():
            results.append(line)

    return {"answers": results}

        
