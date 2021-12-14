import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json


def transform_salary(string_salary):
    """
    Функция принимает строку 120\u202f000 – 160\u202f000 руб. и
    возвращает список вида['валюта', 'мин. величина зп', 'макс. величина зп']
    :param string_salary: '120\u202f000 – 160\u202f000' руб.
    :return: список вида['руб', '120000', '160000']
    """
    salary = []
    if string_salary == 'з/п не указана':
        salary.append(None)
        salary.append(None)
        salary.append(None)
        return salary
    else:
        string_salary = string_salary.replace(' \u200b', '')
        string_salary = string_salary.replace('\u202f', '')
        string_salary = string_salary.replace(' –', '')
    if string_salary.find('руб.') != -1:
        salary.append('RU')
        string_salary = string_salary.replace(' руб.', '')
    elif string_salary.find('USD') != -1:
        salary.append('USD')
        string_salary = string_salary.replace(' USD', '')
    elif string_salary.find('EUR') != -1:
        salary.append('EUR')
        string_salary = string_salary.replace(' EUR', '')

    if string_salary.find('от') == 0:
        string_salary = string_salary.replace('от ', '')
        string_salary = int(string_salary)
        salary.append(string_salary)
        salary.append(None)
    elif string_salary.find('до') == 0:
        string_salary = string_salary.replace('до ', '')
        string_salary = int(string_salary)
        salary.append(None)
        salary.append(string_salary)
    else:
        string_salary = string_salary.split(' ')
        salary.append(int(string_salary[0]))
        salary.append(int(string_salary[1]))
    return salary


url = 'https://hh.ru/search/vacancy?clusters=true&area=113&ored_clusters=true&enable_snippets=true&part_time=employment_project&part_time=employment_part&part_time=temporary_job_true&part_time=from_four_to_six_hours_in_a_day&part_time=only_saturday_and_sunday&part_time=start_after_sixteen&is_part_time_clusters_enabled=true&salary=&text=Python'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
serial_list = []
for j in range(0, 41):
    params = {'page': j}
    response = requests.get(url, params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    serials = dom.find_all('div', {'class', 'vacancy-serp-item'})

    for serial in serials:
        serial_data = {}
        name = serial.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        link = name.get('href')
        name = name.text
        salary = serial.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        try:
            salary = salary.text
        except:
            salary = 'з/п не указана'

        name = name.replace(' \u200b', '')
        serial_data['name'] = name
        link = link.replace('ivanovo.', '')
        serial_data['link'] = link
        serial_data['site'] = 'https://www.hh.ru/'
        salary = transform_salary(salary)
        serial_data['valuta'] = salary[0]
        serial_data['salary from'] = salary[1]
        serial_data['salary up to'] = salary[2]

        serial_list.append(serial_data)

print(serial_list)
filename = 'vacancys.json'
with open(filename, 'w') as f:
    json.dump(serial_list, f, ensure_ascii=False, indent=4, sort_keys=True)
