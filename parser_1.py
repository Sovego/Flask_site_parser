import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.firefox import GeckoDriverManager


def check(driver):
    try:
        elem = driver.find_element(By.CLASS_NAME, 'pagination-widget__page-link_disabled')
        return True
    except NoSuchElementException:
        return False


def parse(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.get(url)
    # Wait page load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'catalog-product')))
    time.sleep(2)
    name = []
    price = []
    while True:
        # Extract information about products
        products = driver.find_elements(By.CLASS_NAME, 'catalog-product')
        for product in products:
            name.append(product.find_element(By.CLASS_NAME, 'catalog-product__name').text)
            tmp = product.find_element(By.CLASS_NAME, 'product-buy')
            price.append(tmp.find_element(By.CLASS_NAME, 'product-buy__price').text)
        # Go to the next page
        try:
            if (check(driver) and not (
                    driver.find_element(By.CLASS_NAME, "pagination-widget__page_active").text == "1")):
                break
            next_page = driver.find_element(By.CLASS_NAME, 'pagination-widget__page-link_next')
            next_page.click()
            # Waiting for the next page to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'catalog-product')))
            time.sleep(2)
        except TimeoutException:
            # If you have reached the last page, exit the loop
            break

    driver.quit()
    df = pd.DataFrame(list(zip(name, price)), columns=['Name', 'price'])
    df.to_csv("result.csv")
    return
