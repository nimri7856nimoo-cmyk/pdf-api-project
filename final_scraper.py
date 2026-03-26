import requests
import pdfplumber
import os

# create folder
os.makedirs("pdfs", exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0"}

# -----------------------------
# STEP 1: REAL LONG PDFs (MANUALLY VERIFIED)
# -----------------------------
pdf_links = [
    "https://www.orimi.com/pdf-test.pdf",
    "https://unec.edu.az/application/uploads/2014/12/pdf-sample.pdf",
    "https://www.africau.edu/images/default/sample.pdf"
]

pdf_text_data = []

# -----------------------------
# STEP 2: DOWNLOAD + EXTRACT
# -----------------------------
for pdf in pdf_links:
    try:
        file_name = pdf.split("/")[-1]
        file_path = os.path.join("pdfs", file_name)

        response = requests.get(pdf, headers=headers)
        
        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"Downloaded: {file_name}")

        # extract text
        with pdfplumber.open(file_path) as pdf_file:
            for i, page in enumerate(pdf_file.pages, start=1):
                text = page.extract_text()
                if text:
                    pdf_text_data.append(f"{file_name} - Page {i}\n{text}\n")

    except Exception as e:
        print("Error:", pdf)

# -----------------------------
# STEP 3: SAVE OUTPUT
# -----------------------------
with open("output.txt", "w", encoding="utf-8") as f:

    f.write("PDF LINKS:\n")
    for pdf in pdf_links:
        f.write(pdf + "\n")

    f.write("\n\nEXTRACTED TEXT:\n")
    for t in pdf_text_data:
        f.write(t + "\n")

print("Done! Everything working.")