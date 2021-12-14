from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient


# пропишем путь до веб-движка и опции его запуска
s = Service('../chromedriver.exe')
chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(service=s, options=chrome_options)
driver.get("https://www.mvideo.ru")

# запустим неявное ожидание
driver.implicitly_wait(10)
# найдем какой-нибудь элементь (логотип), относительно которого будем прокручивать вниз страницу
scroll_down = driver.find_element(By.XPATH, "//img[@class='ng-tns-c269-2']")

# как только найдем данный  элемент, прокрутим на 1300 px вниз для загрузки нужной нам области
if scroll_down:
    driver.execute_script("window.scrollTo(0, 1300)")
# найдем кнопку-ссылку тренды и нажмем ее
link_to_trends = driver.find_element(By.XPATH, "//button/div[@class='content']/span[@class='title'][contains(text(), 'В тренде')]")
try:
    link_to_trends.click()
except Exception as e:
    print(e)
# сохраним всю область с трендовыми продуктами в переменную и представим необходимые нам данные в виде списка словарей
card = driver.find_element(By.XPATH, "//mvid-product-cards-group[@_ngcontent-serverapp-c255='']")
names = card.find_elements(By.CLASS_NAME, 'product-mini-card__name')
prices = card.find_elements(By.CLASS_NAME, 'product-mini-card__price')
trends_data = list(zip(names, prices))

result_list = []
for product in trends_data:
    product_dict = {'name': product[0].text,
                    'link': product[0].find_element(By.XPATH, ".//a").get_attribute('href'),
                    'price': int(product[1].find_element(By.CLASS_NAME, 'price__main-value').text.replace(' ', ''))
                    }
    result_list.append(product_dict)

# загрузим данные в базу данных mongo
client = MongoClient('127.0.0.1', 27017)
db = client['products']
products = db.products

for i in result_list:
    products.insert_one(i)

# прочитаем данные из базы данных mongo
for j in products.find({}):
    print(j)

# вывод:
"""
{'_id': ObjectId('61b79ccf1c5ae784837d494b'), 'name': 'Смартфон Huawei P Smart 2021 4+128GB Crush Green (PPA-LX1)', 'link': 'https://www.mvideo.ru/products/smartfon-huawei-p-smart-2021-4128gb-crush-green-ppa-lx1-30053815', 'price': 15999}
{'_id': ObjectId('61b79ccf1c5ae784837d494c'), 'name': 'Подписка M.Prime на 1 месяц + Яндекс.Плюс', 'link': 'https://www.mvideo.ru/products/podpiska-mprime-na-1-mesyac--yandeksplus-6016151', 'price': 499}
{'_id': ObjectId('61b79ccf1c5ae784837d494d'), 'name': 'Конвектор Hyundai H-HV21-15-UI662', 'link': 'https://www.mvideo.ru/products/konvektor-hyundai-h-hv21-15-ui662-20055370', 'price': 3990}
{'_id': ObjectId('61b79ccf1c5ae784837d494e'), 'name': 'Смарт-часы Samsung Galaxy Watch3 45mm Черные (SM-R840N)', 'link': 'https://www.mvideo.ru/products/smart-chasy-samsung-galaxy-watch3-45mm-chernye-sm-r840n-30051392', 'price': 25499}
{'_id': ObjectId('61b79ccf1c5ae784837d494f'), 'name': 'Электрогриль Tefal Supergrill GC450B32', 'link': 'https://www.mvideo.ru/products/elektrogril-tefal-supergrill-gc450b32-20036709', 'price': 9999}
{'_id': ObjectId('61b79ccf1c5ae784837d4950'), 'name': 'Электрочайник Tefal Sense KO693110', 'link': 'https://www.mvideo.ru/products/elektrochainik-tefal-sense-ko693110-20074031', 'price': 3999}
{'_id': ObjectId('61b79ccf1c5ae784837d4951'), 'name': 'Кофемашина капсульного типа Nespresso Vertuo Next GCV1 Cherry Red', 'link': 'https://www.mvideo.ru/products/kofemashina-kapsulnogo-tipa-nespresso-vertuo-next-gcv1-cherry-red-20070575', 'price': 6999}
{'_id': ObjectId('61b79ccf1c5ae784837d4952'), 'name': 'Ручной отпариватель Philips STH3020/10', 'link': 'https://www.mvideo.ru/products/ruchnoi-otparivatel-philips-sth3020-10-20072378', 'price': 3999}
{'_id': ObjectId('61b79ccf1c5ae784837d4953'), 'name': 'Электробритва Philips S5586/66', 'link': 'https://www.mvideo.ru/products/elektrobritva-philips-s5586-66-20071329', 'price': 9999}
{'_id': ObjectId('61b79ccf1c5ae784837d4954'), 'name': 'Электрическая зубная щетка Braun Oral-B 750/D16.513.UX', 'link': 'https://www.mvideo.ru/products/elektricheskaya-zubnaya-shhetka-braun-oral-b-750-d16513ux-20061206', 'price': 2999}
{'_id': ObjectId('61b79ccf1c5ae784837d4955'), 'name': 'Триммер Rowenta Forever Sharp TN6000F(4/5)', 'link': 'https://www.mvideo.ru/products/trimmer-rowenta-forever-sharp-tn6000f4-5-20061772', 'price': 1999}
{'_id': ObjectId('61b79ccf1c5ae784837d4956'), 'name': 'Робот-пылесос Tefal Smart Force X-plorer RG6825WH', 'link': 'https://www.mvideo.ru/products/robot-pylesos-tefal-smart-force-x-plorer-rg6825wh-20063304', 'price': 8999}
{'_id': ObjectId('61b79ccf1c5ae784837d4957'), 'name': 'Пылесос ручной (handstick) Tefal X-Force Flex 8.60 Aqua TY9690WO', 'link': 'https://www.mvideo.ru/products/pylesos-ruchnoi-handstick-tefal-x-force-flex-860-aqua-ty9690wo-20071482', 'price': 22999}
{'_id': ObjectId('61b79ccf1c5ae784837d4958'), 'name': 'Микроволновая печь соло Midea AM720KFR-B/S', 'link': 'https://www.mvideo.ru/products/mikrovolnovaya-pech-solo-midea-am720kfr-b-s-20052031', 'price': 8999}
"""
