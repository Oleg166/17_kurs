import requests
import json


service = 'https://api.github.com'
user = 'oleg166'
req = requests.get(f'{service}/users/{user}/repos')

# Список всех репозиториев
for i in req.json():
    print(i['name'])

# Сохранить JSON-вывод в файле *.json
with open('data1.json', 'w') as f:
    json.dump(req.json(), f)
