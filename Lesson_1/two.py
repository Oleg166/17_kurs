import requests
import json


url = 'https://api.nasa.gov/'
service = 'planetary/apod'
key = {'api_key': 'example'}

# результаты запроса
req = requests.get(f'{url}{service}', params=key)
data = json.loads(req.text)
print(data)

# запись ответа сервера в файл
with open('data2.json', 'w') as f:
    json.dump(req.json(), f)
