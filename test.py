from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection

SBR_WEBDRIVER = 'https://brd-customer-hl_8a10678a-zone-scraping_browser3:tc2g8cce59c7@brd.superproxy.io:9515'

def extract_product_details(driver):
    product_details = {}

    try:
        # Wait for the title to be available and extract it
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "productTitle"))
        )
        product_details['title'] = title_element.text.strip()

        # Wait for the description to be available and extract it
        description_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".a-section.a-spacing-none.column-description p"))
        )
        product_details['description'] = description_element.text.strip()

        # Wait for the price to be available and extract it
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "priceblock_ourprice"))
        )
        product_details['price'] = price_element.text.strip()

        # Check for any promotions
        try:
            promotion_element = driver.find_element(By.ID, "promoPriceBlockMessage_feature_div")
            product_details['promotion'] = promotion_element.text.strip()
        except:
            product_details['promotion'] = "No promotions available"

    except Exception as e:
        print(f"An error occurred: {e}")

    return product_details


def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating to product page...')
        driver.get('https://www.amazon.com/JBL-Tune-Flex-Wireless-Cancelling/dp/B0C1QNRGHC/')
        
        print('Navigated! Extracting product details...')
        product_details = extract_product_details(driver)
        
        print('Product Details:', product_details)


if __name__ == '__main__':
    main()