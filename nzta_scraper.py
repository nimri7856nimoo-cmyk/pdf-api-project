import requests
from bs4 import BeautifulSoup

url = "https://www.nzta.govt.nz/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

if soup.title:
    print("Page Title:", soup.title.text)
else:
    print("Title not found (dynamic site)")