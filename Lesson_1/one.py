import requests
import json


service = 'https://api.github.com'
user = 'oleg166'
req = requests.get(f'{service}/users/{user}/repos')

# список всех репозиториев
for i in req.json():
    print(i['name'])

"""
17_kurs
framepaper
HTML_CSS_29.05.2020
Intergalactic_Entertainment
kellolo-js-2-21-1209
Preparing
Python_Algos
Python_Basics_17.12.2019
"""

# сохранение JSON-вывода в файле *.json
with open('data1.json', 'w') as f:
    json.dump(req.json(), f)
