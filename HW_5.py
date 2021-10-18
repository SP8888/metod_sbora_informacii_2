# Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД. Сайт можно выбрать и свой.
#Главный критерий выбора: динамически загружаемые товары
from pprint import pprint
from lxml import html
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions as se
import time


chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")

chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
driver.get('https://www.mvideo.ru/')
time.sleep(5)
wait = WebDriverWait(driver, 10)

# убирает всплывающее окно, причем окно то есть то нет
button = wait.until(EC.presence_of_element_located((By.XPATH,'//mvid-icon[contains(@class,"modal-layout__close ng-tns-c72-1 ng-star-interesed")]')))
button.click()
time.sleep(4)

# прокручивает экран вниз пока не становится видна кнопка "в тренде"
driver.execute_script("window.scrollTo(0, 1500);")

time.sleep(4)

# нажимает кнопку в "тренде"
button = wait.until(EC.presence_of_element_located((By.XPATH,'//span [@class="title"][contains(text(), "В тренде")]')))
button.click()

time.sleep(4)
# прокручивает вправо список товаров
while True:
    try:
        button = driver.find_element(By.XPATH,"//mvid-shelf-group//button [@class='btn forward mv-icon-button--primary mv-icon-button--shadow mv-icon-button--medium mv-button mv-icon-button'] /mvid-icon [@type='chevron_right']")
        button.click()  # потому что два элемента находятся, первый непонятно где
        time.sleep(4)
    except se.ElementNotInteractableException:
        break


time.sleep(4)

items = driver.find_element(By.XPATH,"//mvid-shelf-group//mvid-product-cards-group/div[@class='title']")

items_list = []

for item in items:
    item_info = {}
    item_link = item.find_element(By.TAG_NAME,'a').get_attribute("href")
    item_title = item.find_element(By.TAG_NAME,'a').text
    item_info['Title'] = item_title
    item_info['link'] = item_link

    items_list.append(item_info)

pprint(items_list)
driver.close()



#//mvid-shelf-group//mvid-product-cards-group
#//mvid-shelf-group/*//button[contains(@class, 'btn forwad')]/mvid-icon[@type = 'chevron_right']

#//button [@class="btn forward mv-icon-button--primary mv-icon-button--shadow mv-icon-button--medium mv-button mv-icon-button"] /mvid-icon [@type="chevron_right"]