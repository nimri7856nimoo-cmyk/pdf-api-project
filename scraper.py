import requests
from bs4 import BeautifulSoup
import pdfplumber
import os
import time

# -----------------------------
# SETUP
# -----------------------------
os.makedirs("pdfs", exist_ok=True)
headers = {"User-Agent": "Mozilla/5.0"}

pdf_site_url = "https://file-examples.com/index.php/sample-documents-download/sample-pdf-download/"

# -----------------------------
# STEP 1: LOAD WEBSITE
# -----------------------------
response = requests.get(pdf_site_url, headers=headers)

pdf_links = []

if response.status_code == 200:
    print("Website Loaded Successfully")
    soup = BeautifulSoup(response.text, "html.parser")
    
    # find all <a> tags that contain ".pdf"
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and ".pdf" in href and href.startswith("https://file-examples.com"):
            pdf_links.append(href)
else:
    print("Error loading website")

print(f"Total PDFs Found: {len(pdf_links)}")

# -----------------------------
# STEP 2: DOWNLOAD PDF + EXTRACT TEXT
# -----------------------------
pdf_text_data = []

for pdf_url in pdf_links[:3]:  # first 3 PDFs
    try:
        file_name = pdf_url.split("/")[-1]
        file_path = os.path.join("pdfs", file_name)
        
        # download pdf
        pdf_response = requests.get(pdf_url, headers=headers)
        with open(file_path, "wb") as f:
            f.write(pdf_response.content)
        
        print(f"Downloaded: {file_name}")
        
        # extract text
        with pdfplumber.open(file_path) as pdf_file:
            for i, page in enumerate(pdf_file.pages, start=1):
                text = page.extract_text()
                if text:
                    pdf_text_data.append(f"{file_name} - Page {i}\n{text}\n")
        
        # small delay to avoid server issues
        time.sleep(1)
        
    except Exception as e:
        print("Error processing PDF:", pdf_url)
        print(e)

# -----------------------------
# STEP 3: SAVE OUTPUT
# -----------------------------
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("PDF LINKS:\n")
    for pdf in pdf_links[:3]:
        f.write(pdf + "\n")
    
    f.write("\n\nEXTRACTED PDF TEXT:\n")
    for t in pdf_text_data:
        f.write(t + "\n")

print("Done! PDFs downloaded and text extracted.")