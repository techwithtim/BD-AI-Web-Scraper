# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set up the WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (optional)

service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the website
url = "https://techwithtim.net/"
driver.get(url)

# Allow the page to load
time.sleep(3)

# Find the topics container
try:
    topics_container = driver.find_element(By.CLASS_NAME, "pages__TagList-sc-1o7d36l-1")

    # Extract all topics
    topics_elements = topics_container.find_elements(
        By.CLASS_NAME, "tag__TagContainer-sc-3f52y0-0"
    )
    topics = [topic.text for topic in topics_elements]

    # Print the extracted topics
    print("Extracted topics:")
    for topic in topics:
        print(topic)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the WebDriver
    driver.quit()
