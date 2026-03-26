from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Open browser
driver = webdriver.Chrome()

# Open website
driver.get("https://www.nzta.govt.nz/")

# Wait for page load
time.sleep(5)

# Get title
print("Title:", driver.title)

# Get all links
links = driver.find_elements(By.TAG_NAME, "a")

for link in links:
    href = link.get_attribute("href")
    if href and ".pdf" in href:
        print("PDF:", href)

driver.quit()