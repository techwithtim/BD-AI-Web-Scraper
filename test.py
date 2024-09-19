# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# URL of the target page
url = "https://www.trueclassictees.com/en-my/collections/polos"

# Open the URL
driver.get(url)

# Wait for the page to load completely
time.sleep(5)  # Adjust the sleep time as needed based on your internet speed

# Extract product elements
product_elements = driver.find_elements(By.CSS_SELECTOR, ".product-card")

# Initialize lists to store product titles and prices
products = []
prices = []

# Loop through each product element and extract the required information
for product in product_elements:
    try:
        # Extract product title
        title_element = product.find_element(By.CSS_SELECTOR, ".product-card__title")
        title = title_element.text
        products.append(title)
    except Exception as e:
        print(f"Error extracting title: {e}")
        products.append("N/A")

    try:
        # Extract product price
        price_element = product.find_element(
            By.CSS_SELECTOR, ".product-card__price .price"
        )
        price = price_element.text
        prices.append(price)
    except Exception as e:
        print(f"Error extracting price: {e}")
        prices.append("N/A")

# Print the extracted products and prices
for product, price in zip(products, prices):
    print(f"Product: {product}, Price: {price}")

# Close the WebDriver
driver.quit()
