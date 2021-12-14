from lxml import html
import requests
from pymongo import MongoClient

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
url = 'https://lenta.ru/'

response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)

news = []


def transform(fname, flink, fdate, ftime):
    new = {}
    fname = fname.replace('\xa0', ' ')
    flink = url + flink

    new['source'] = url
    new['name'] = fname
    new['link'] = flink
    new['date'] = fdate
    new['time'] = ftime
    return new
    

# собираем данные о заглавной новости
item_one = dom.xpath("//div[@class='span8 js-main__content']//div[@class='first-item']")
for i in item_one:
    name = i.xpath('./h2/a/text()')[0]
    link = i.xpath("./a/@href")[0]
    date = i.xpath("./h2/a/time/@title")[0]
    time = i.xpath("./h2/a/time/text()")[0]

    new = transform(name, link, date, time)
    news.append(new)

# собираем данные о других 9 новостях
items = dom.xpath("//div[@class='span8 js-main__content']//div[@class='item']/a")
for i in items:
    new = {}
    name = i.xpath('./text()')[0]
    link = i.xpath("./@href")[0]
    date = i.xpath("./time/@title")[0]
    time = i.xpath("./time/text()")[0]

    new = transform(name, link, date, time)
    news.append(new)

# запишем данные в базу данных mongo
client = MongoClient('127.0.0.1', 27017)
db = client['news']
news_of_db = db.news_of_db

for i in news:
    news_of_db.insert_one(i)

# прочитаем данные из базы данных mongo
for j in news_of_db.find({}):
    print(j)

# вывод:
"""
{'_id': ObjectId('61b60f3038472f4cfb7d8aa7'), 'source': 'https://lenta.ru/', 'name': 'В Ливии заявили о тысячах находящихся в стране «вагнеровцах»', 'link': 'https://lenta.ru//news/2021/12/12/vagner/', 'date': '12 декабря 2021', 'time': '17:15'}
{'_id': ObjectId('61b60f3038472f4cfb7d8aa8'), 'source': 'https://lenta.ru/', 'name': 'Полиция задержала надругавшегося над 14-летней российской школьницей мигранта', 'link': 'https://lenta.ru//news/2021/12/12/pedofil/', 'date': '12 декабря 2021', 'time': '18:01'}
{'_id': ObjectId('61b60f3038472f4cfb7d8aa9'), 'source': 'https://lenta.ru/', 'name': 'Медведев назвал обновленную Конституцию обеспечивающей развитие России', 'link': 'https://lenta.ru//news/2021/12/12/medvedev_konst/', 'date': '12 декабря 2021', 'time': '17:52'}
{'_id': ObjectId('61b60f3038472f4cfb7d8aaa'), 'source': 'https://lenta.ru/', 'name': 'В Госдепе заявили о готовящихся контрмерах на случай вторжения России на Украину', 'link': 'https://lenta.ru//news/2021/12/12/blinken/', 'date': '12 декабря 2021', 'time': '17:52'}
{'_id': ObjectId('61b60f3038472f4cfb7d8aab'), 'source': 'https://lenta.ru/', 'name': 'Замсекретаря Совбеза России ответил США русской пословицей', 'link': 'https://lenta.ru//news/2021/12/12/democracy/', 'date': '12 декабря 2021', 'time': '17:45'}
{'_id': ObjectId('61b60f3038472f4cfb7d8aac'), 'source': 'https://lenta.ru/', 'name': 'Комета Леонарда максимально сблизилась с Землей', 'link': 'https://lenta.ru//news/2021/12/12/kometa/', 'date': '12 декабря 2021', 'time': '17:44'}
{'_id': ObjectId('61b60f3038472f4cfb7d8aad'), 'source': 'https://lenta.ru/', 'name': 'Ферстаппен опередил Хэмилтона и стал победителем «Формулы-1»', 'link': 'https://lenta.ru//news/2021/12/12/f1/', 'date': '12 декабря 2021', 'time': '17:40'}
{'_id': ObjectId('61b60f3038472f4cfb7d8aae'), 'source': 'https://lenta.ru/', 'name': 'В Совбезе уличили США в создании «цифрового НАТО»', 'link': 'https://lenta.ru//news/2021/12/12/online_nato/', 'date': '12 декабря 2021', 'time': '17:38'}
{'_id': ObjectId('61b60f3038472f4cfb7d8aaf'), 'source': 'https://lenta.ru/', 'name': 'В московской больнице пациента обокрали во время операции', 'link': 'https://lenta.ru//news/2021/12/12/stolen/', 'date': '12 декабря 2021', 'time': '17:31'}
{'_id': ObjectId('61b60f3038472f4cfb7d8ab0'), 'source': 'https://lenta.ru/', 'name': 'Путин описал последствия распада России', 'link': 'https://lenta.ru//news/2021/12/12/yugoslavia/', 'date': '12 декабря 2021', 'time': '16:26'}
"""
