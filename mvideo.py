from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
in_trend_db = db.in_trend

chrome_options = Options()
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
driver.implicitly_wait(5)

driver.get('https://www.mvideo.ru/')


body = driver.find_element(By.TAG_NAME, "body")

while True:
    try:
        elem = driver.find_element(By.XPATH, "//span[contains(text(), 'В тренде')]")
        elem.click()
        break
    except:
        body.send_keys(Keys.PAGE_DOWN)

names_lst = driver.find_elements(By.XPATH, "//mvid-shelf-group//div[contains(@class, 'product-mini-card__name')]//a")
price_lst = driver.find_elements(By.XPATH, "//mvid-shelf-group//span[contains(@class, 'price__main-value')]")

for i in range(len(price_lst)):
    items = {'name': names_lst[i].text,
             'price': int(price_lst[i].text.replace(' ', '')),
             'link': names_lst[i].get_attribute('href')}

    in_trend_db.update_one({'link': items['link']}, {'$set': items}, upsert=True)

driver.quit()
