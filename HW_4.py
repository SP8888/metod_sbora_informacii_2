#Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
#название источника;
#наименование новости;
#ссылку на новость;
#дата публикации.

from pprint import pprint
from lxml import html
import requests
import pandas as pd
import pymongo
from pymongo import MongoClient

# скачиваем заглавную страницу и формируем дом
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
response = requests.get("https://news.mail.ru/")
dom = html.fromstring(response.text)

# собираем ссылки на контейнеры с новостями, получается три типа контейнеров - с большим фото, с маленьким фото и совсем без фото
link = dom.xpath("//li/a[@class='list__text']/@href")
link_foto = dom.xpath('//a [@class="photo photo_full photo_scale js-topnews__item"]/@href')
link_foto_small = dom.xpath('//a [@class="photo photo_small photo_scale photo_full js-topnews__item"]/@href')

# все ссылки обьеденяем в один список
for lin in link_foto:
    link.append(lin)
for lin in link_foto_small:
    link.append(lin)

# собираем данные из контейнеров, внутри они все одинаковые и формируем dataFrame
all_news = []
i=0
while i < len(link):
    news = {}
    response = requests.get(link[i])
    dom = html.fromstring(response.text)
    source = dom.xpath("//a [@class='link color_gray breadcrumbs__link']/span/text()")
    novost = dom.xpath("//h1/text()")
    data = dom.xpath("//span [@class='note__text breadcrumbs__text js-ago']/@datetime")

    news['novost'] = novost
    news['link'] = link[i]
    news['source'] = source
    news['data'] = data
    all_news.append(news)
    i += 1

df_news = pd.DataFrame(all_news)


# создаем и заполняем базу данных
client = MongoClient('127.0.0.1', 27017)
db = client['news']
news = db.news

for index, row in df_news.iterrows(): # try - except внутри цикла for что бы при повторной записи все элементы проверились на запись в базу иначе обрывается на первом не новом элементе
    try:
        news .insert_one({
        "_id": row['link'],
        "name": row['novost'],
        "link": row['link'],
        "source": row['source'],
        "data": row['data']
        })
    except pymongo.errors.DuplicateKeyError:
        print('Document already exist')

for doc in news.find({}):    # распечатывает содержимое базы данных вместе со старыми новостями, которых уже нет на странице, если запуск программы не первый
    pprint(doc)

