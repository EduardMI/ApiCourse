import requests
from lxml import html
from pymongo import MongoClient

# создание БД
client = MongoClient('127.0.0.1', 27017)
db = client['mail_news']
news_db = db.news

# получение списка ссылок новостей
url = 'https://news.mail.ru/'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

# полностью выбирает и вариант --> //div[@class='js-module']//a
# links_news = dom.xpath("//div[@class='js-module']//a/@href")
links_news = dom.xpath("//div[@class='js-module']//a[contains(@class, 'list__text')]/@href | "
                       "//div[@class='js-module']//a[contains(@class, 'js-topnews__item')]/@href")

# собираем информацию по каждой из сылок
for item in links_news:
    response = requests.get(item, headers=headers)
    dom = html.fromstring(response.text)

    name_news = dom.xpath("//div[contains(@class, 'js-article')]//h1/text()")
    date_news = dom.xpath("//div[contains(@class, 'js-article')]//span[@datetime]/@datetime")
    # date_news = dom.xpath("//div[contains(@class, 'js-article')]//span[@datetime]/text()")
    source_news = dom.xpath("//div[contains(@class, 'js-article')]//span[@class='link__text']/text()")

    list_news = {'source_news': source_news[0],
                 'name_news': name_news[0],
                 'link_news': item,
                 'date_news': date_news[0]}

    # записываем словарь собранных данных в БД
    news_db.update_one({'link_news': list_news['link_news']}, {'$set': list_news}, upsert=True)
