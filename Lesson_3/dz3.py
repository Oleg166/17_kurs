from pymongo import MongoClient
from pprint import pprint
import json

# создание базы данных в mongo
client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
vac = db.vac

# добавление данных из файла из предыдущего задания в базу данных mongo
with open('../Lesson_2/vacancys.json') as f:
    data = json.load(f)
    for i in data:
        vac.insert_one(i)


# функция для добавления только новых записей (проверка по ссылке на вакансию)


def add_new_vac(vacansy):
    link = vacansy['link']
    if vac.count_documents({'link': link}) > 0:
        print('not new vacancy')
    else:
        vac.insert_one(vacansy)


# проверим работоспособность функции
check = {
        "link": "https://hh.ru/vacancy/49588066?from=vacancy_search_list&query=Python",
        "name": "Разработчик алгоритмов глубокого машинного обучения (ML, нейронные сети)",
        "salary from": 2000000,
        "salary up to": 3000000,
        "site": "https://www.hh.ru/",
        "valuta": "RU"
    }

add_new_vac(check)

# функция, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# подготовим данные
# переведем зарплату в евро в рубли
for odc in vac.find({'valuta': 'EUR'}):
    id = odc['_id']
    sf = odc['salary from']
    su = odc['salary up to']
    if sf is None:
        pass
    else:
        sf = sf * 83
    if su is None:
        pass
    else:
        su = su * 83
    new_data = {
        'salary from': sf,
        'salary up to': su,
        'valuta': 'RU'
    }
    vac.update_one({'_id': id}, {'$set': new_data})

# переведем зарплату в долларах в рубли
for odc in vac.find({'valuta': 'USD'}):
    id = odc['_id']
    sf = odc['salary from']
    su = odc['salary up to']
    if sf is None:
        pass
    else:
        sf = sf * 74
    if su is None:
        pass
    else:
        su = su * 74
    new_data = {
        'salary from': sf,
        'salary up to': su,
        'valuta': 'RU'
    }
    vac.update_one({'_id': id}, {'$set': new_data})

# функция, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
try:
    value_salary = int(input("Введите величину зарплаты в рублях, выше которой Вы рассматриваете вакансии: "))
    for doc in vac.find({'$or': [{'salary up to': {'$gt': value_salary}}, {'salary from': {'$gt': value_salary}}]}):
        pprint(doc)
except:
    print("Введите число!!!")
