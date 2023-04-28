from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

def check(driver):
    try:
     elem = driver.find_element(By.CLASS_NAME,'pagination-widget__page-link_disabled')
     return True
    except NoSuchElementException:
     return False

def parse(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.get(url)
    # Ждем загрузки страницы
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'catalog-product')))
    time.sleep(2)
    name = []
    price = []
    while True:
        # Извлекаем информацию о товарах
        products = driver.find_elements(By.CLASS_NAME,'catalog-product')
        for product in products:
            name.append(product.find_element(By.CLASS_NAME,'catalog-product__name').text)
            tmp = product.find_element(By.CLASS_NAME,'product-buy')
            price.append(tmp.find_element(By.CLASS_NAME,'product-buy__price').text)
        # Переходим на следующую страницу
        try:
            if (check(driver) and not (driver.find_element(By.CLASS_NAME,"pagination-widget__page_active").text=="1")):
                break
            next_page = driver.find_element(By.CLASS_NAME,'pagination-widget__page-link_next')
            next_page.click()
            # Ждем загрузки следующей страницы
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'catalog-product')))
            time.sleep(2)
        except:
            # Если достигли последней страницы, выходим из цикла
            break

    driver.quit()
    df = pd.DataFrame(list(zip(name, price)), columns =['Name', 'price'])
    df.to_csv("result.csv")
    return
