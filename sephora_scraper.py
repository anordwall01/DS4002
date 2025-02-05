import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless (no UI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Correct Chromedriver path for Ubuntu
service = Service("/usr/local/bin/chromedriver")  # Your chromedriver path

# Initialize WebDriver with the service and options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Sephora product URL
url = "https://www.sephora.com/product/rare-beauty-by-selena-gomez-perfect-strokes-universal-volumizing-mascara-P475599?skuId=2474138"
driver.get(url)
time.sleep(5)  # Allow page to load

# Scroll down to load reviews
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

# Extract all review blocks
reviews = driver.find_elements(By.XPATH, "//div[@class='css-1v5c5k7']//div[@class='css-12ymk3y']")

review_data = []

# Extract review details
for review in reviews:
    try:
        title = review.find_element(By.XPATH, ".//h3[contains(@class, 'css-88p8ea')]").text.strip()
    except:
        title = "N/A"

    try:
        text = review.find_element(By.XPATH, ".//div[contains(@class, 'css-2482tk')]").text.strip()
    except:
        text = "N/A"

    try:
        stars = review.find_element(By.XPATH, ".//div[contains(@class, 'css-1yopk1y')]").get_attribute("aria-label")
    except:
        stars = "N/A"

    try:
        username = review.find_element(By.XPATH, ".//a[@data-at='nickname']").text.strip()
    except:
        username = "N/A"

    try:
        date = review.find_element(By.XPATH, ".//span[contains(@class, 'css-1rasscf')]").text.strip()
    except:
        date = "N/A"

    review_data.append({
        "Title": title,
        "Stars": stars,
        "Text": text,
        "Username": username,
        "Date": date
    })

# Save to CSV
df = pd.DataFrame(review_data)
df.to_csv("sephora_reviews.csv", index=False)

# Close the driver
driver.quit()

print("Reviews scraped and saved to 'sephora_reviews.csv'")
