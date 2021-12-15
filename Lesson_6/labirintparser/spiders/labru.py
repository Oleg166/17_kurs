import scrapy
from scrapy.http import HtmlResponse
from labirintparser.items import LabirintparserItem


class LabruSpider(scrapy.Spider):
    name = 'labru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/python/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@class="pagination-next__text"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@class="product-title-link"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        # название книги берем из поля, где не прописаны авторы
        name = response.xpath('//div[@id="product-about"]/h2/text()').get()
        name = name[19:-1]

        # ссылку берем из значения ссылки для каждой страницы
        link = response.url

        # у книги авторов бывает несколько, поэтому они сохраняются в виде списка
        list_authors = []
        count_authors = response.xpath('count(//a[@data-event-label="author"])').get()
        count_authors = count_authors[0:1]
        count_authors = int(count_authors)
        for j in range(1, count_authors+1):
            author_xpath = f'//a[@data-event-label="author"][{j}]/text()'
            author = response.xpath(author_xpath).get()
            list_authors.append(author)

        # у книги может быть четыре варианта представления цены, поэтому она сохраняется в виде списка
        list_xpath = ['//span[@class="buying-price-val-number"]/text()',
                      '//span[@class="buying-pricenew-val-number"]/text()',
                      '//span[@class="buying-priceold-val-number"]/text()']
        list_price = []
        for i in range(0, len(list_xpath)):
            price = response.xpath(list_xpath[i]).get()
            try:
                price = int(price)
            except TypeError:
                price = None
            list_price.append(price)

        rating = response.xpath('//div[@id="rate"]/text()').get()
        rating = float(rating)

        item = LabirintparserItem(name=name, link=link, authors=list_authors, price=list_price, rating=rating)
        yield item

# пример данных в базе
"""
{'_id': ObjectId('61ba44b2eda375952c96637d'), 'name': 'Python 3. Самое необходимое', 'link': 'https://www.labirint.ru/books/662231/', 'authors': ['Прохоренок Николай Анатольевич', 'Дронов Владимир Александрович'], 'price': [None, 920, 1180], 'rating': 3.0}
{'_id': ObjectId('61ba44b2eda375952c96637e'), 'name': 'Глубокое обучение. Легкая разработка проектов на Python', 'link': 'https://www.labirint.ru/books/788336/', 'authors': ['Вейдман Сет'], 'price': [None, 2295, 2942], 'rating': 0.0}
{'_id': ObjectId('61ba44b2eda375952c96637f'), 'name': 'Python и DevOps. Ключ к автоматизации Linux', 'link': 'https://www.labirint.ru/books/832978/', 'authors': ['Гифт Ной', 'Деза Альфредо', 'Берман Кеннеди'], 'price': [None, 2026, 2598], 'rating': 0.0}
{'_id': ObjectId('61ba44b2eda375952c966380'), 'name': 'Анализ социальных медиа на Python', 'link': 'https://www.labirint.ru/books/620685/', 'authors': ['Бонцанини Марко'], 'price': [None, 1463, 1876], 'rating': 5.27}
{'_id': ObjectId('61ba44b2eda375952c966381'), 'name': 'Путь Python. Черный пояс по разработке, масштабированию, тестированию и развертыванию', 'link': 'https://www.labirint.ru/books/713544/', 'authors': ['Данжу Джульен'], 'price': [None, 1026, 1315], 'rating': 4.83}
{'_id': ObjectId('61ba44b2eda375952c966382'), 'name': 'Глубокое обучение на Python', 'link': 'https://www.labirint.ru/books/645742/', 'authors': ['Шолле Франсуа'], 'price': [None, 1177, 1509], 'rating': 8.55}
{'_id': ObjectId('61ba44b2eda375952c966383'), 'name': 'Построение систем машинного обучения на языке Python', 'link': 'https://www.labirint.ru/books/498681/', 'authors': ['Коэльо Луис Педро', 'Ричарт Вилли'], 'price': [None, 1281, 1642], 'rating': 6.75}
{'_id': ObjectId('61ba44b3eda375952c966384'), 'name': 'Легкий способ выучить Python 3 еще глубже', 'link': 'https://www.labirint.ru/books/739701/', 'authors': ['Шоу Зед А.'], 'price': [None, 740, 949], 'rating': 10.0}
{'_id': ObjectId('61ba44b3eda375952c966385'), 'name': 'Spark в действии. С примерами Java, Python и Scala', 'link': 'https://www.labirint.ru/books/784236/', 'authors': ['Перрен Жан-Жорж'], 'price': [None, 3111, 3988], 'rating': 0.0}
{'_id': ObjectId('61ba44b3eda375952c966386'), 'name': 'Глубокое обучение с подкреплением на Python. OpenAI Gym и TensorFlow для профи', 'link': 'https://www.labirint.ru/books/710005/', 'authors': ['Равичандиран Судхарсан'], 'price': [None, 1173, 1504], 'rating': 4.0}
{'_id': ObjectId('61ba44b3eda375952c966387'), 'name': 'Научное программирование на Python', 'link': 'https://www.labirint.ru/books/799449/', 'authors': ['Хилл Кристиан'], 'price': [None, 2927, 3752], 'rating': 0.0}
{'_id': ObjectId('61ba44b3eda375952c966388'), 'name': 'Разработка геоприложений на языке Python', 'link': 'https://www.labirint.ru/books/560587/', 'authors': ['Вестра Эрик'], 'price': [None, 1555, 1993], 'rating': 8.5}
{'_id': ObjectId('61ba44b3eda375952c966389'), 'name': 'Python. Великое программирование в Minecraft', 'link': 'https://www.labirint.ru/books/773613/', 'authors': ['Корягин Андрей Владимирович', 'Корягина Алиса Витальевна'], 'price': [None, 673, 863], 'rating': 9.0}
{'_id': ObjectId('61ba44b3eda375952c96638a'), 'name': 'Программирование на Python для начинающих', 'link': 'https://www.labirint.ru/books/503717/', 'authors': ['МакГрат Майк'], 'price': [None, 600, 769], 'rating': 7.67}
{'_id': ObjectId('61ba44b3eda375952c96638b'), 'name': 'Чистый Python. Тонкости программирования для профи', 'link': 'https://www.labirint.ru/books/654838/', 'authors': ['Бейдер Дэн'], 'price': [None, 1168, 1498], 'rating': 7.5}
{'_id': ObjectId('61ba44b3eda375952c96638c'), 'name': '“Непрактичный” Python. Занимательные проекты для тех, кто хочет поумнеть', 'link': 'https://www.labirint.ru/books/785345/', 'authors': ['Воган Ли'], 'price': [None, 944, 1210], 'rating': 0.0}
{'_id': ObjectId('61ba44b3eda375952c96638d'), 'name': 'Современный скрапинг веб-сайтов с помощью Python', 'link': 'https://www.labirint.ru/books/790533/', 'authors': ['Митчелл Райан'], 'price': [None, 1765, 2263], 'rating': 0.0}
{'_id': ObjectId('61ba44b3eda375952c96638e'), 'name': 'Основы Python. Научитесь мыслить как программист', 'link': 'https://www.labirint.ru/books/792480/', 'authors': ['Дауни Аллен Б.'], 'price': [None, 1046, 1341], 'rating': 6.0}
{'_id': ObjectId('61ba44b3eda375952c96638f'), 'name': 'Искусственный интеллект с примерами на Python. Создание приложений искусственного интеллекта', 'link': 'https://www.labirint.ru/books/681061/', 'authors': ['Джоши Пратик'], 'price': [None, 2696, 3456], 'rating': 5.69}
{'_id': ObjectId('61ba44b3eda375952c966390'), 'name': 'Крупномасштабное машинное обучение вместе с Python', 'link': 'https://www.labirint.ru/books/612986/', 'authors': ['Шарден Бастиан', 'Боскетти Альберто', 'Массарон Лука'], 'price': [None, 1463, 1876], 'rating': 0.0}
{'_id': ObjectId('61ba44b3eda375952c966391'), 'name': 'Байесовские модели. Байесовская статистика на языке Python', 'link': 'https://www.labirint.ru/books/659624/', 'authors': ['Дауни Аллен Б.'], 'price': [None, 1187, 1522], 'rating': 9.33}
{'_id': ObjectId('61ba44b3eda375952c966392'), 'name': 'Криптография и взлом шифров на Python', 'link': 'https://www.labirint.ru/books/749459/', 'authors': ['Свейгарт Эл'], 'price': [None, 2022, 2592], 'rating': 8.67}
{'_id': ObjectId('61ba44b3eda375952c966393'), 'name': 'Секреты Python Pro', 'link': 'https://www.labirint.ru/books/784210/', 'authors': ['Хиллард Дейн'], 'price': [None, 1888, 2421], 'rating': 0.0}
{'_id': ObjectId('61ba44b3eda375952c966394'), 'name': 'Профессиональная разработка на Python', 'link': 'https://www.labirint.ru/books/798005/', 'authors': ['Уилкс Мэттью'], 'price': [None, 3111, 3988], 'rating': 0.0}
{'_id': ObjectId('61ba44b3eda375952c966395'), 'name': 'Анализ поведенческих данных на R и PYTHON', 'link': 'https://www.labirint.ru/books/828096/', 'authors': ['Бюиссон Флоран'], 'price': [None, 2377, 3048], 'rating': 0.0}
{'_id': ObjectId('61ba44b4eda375952c966396'), 'name': 'Изучаем квантовые вычисления на Python и Q#', 'link': 'https://www.labirint.ru/books/817237/', 'authors': ['Кайзер Сара', 'Гранад Кристофер'], 'price': [None, 2561, 3283], 'rating': 0.0}
{'_id': ObjectId('61ba44b4eda375952c966397'), 'name': 'Аналитика в Power BI с помощью R и Python', 'link': 'https://www.labirint.ru/books/812712/', 'authors': ['Уэйд Райан'], 'price': [None, 2377, 3048], 'rating': 0.0}
{'_id': ObjectId('61ba44b4eda375952c966398'), 'name': 'Black Hat Python. Программирование для хакеров и пентестеров', 'link': 'https://www.labirint.ru/books/834362/', 'authors': ['Зейтц Джастин', 'Арнольд Тим'], 'price': [None, 1336, 1713], 'rating': 0.0}
{'_id': ObjectId('61ba44b4eda375952c966399'), 'name': 'Простой Python. Современный стиль программирования', 'link': 'https://www.labirint.ru/books/777260/', 'authors': ['Любанович Билл'], 'price': [None, 1617, 2073], 'rating': 10.0}
{'_id': ObjectId('61ba44b4eda375952c96639a'), 'name': 'Программируем на Python', 'link': 'https://www.labirint.ru/books/311244/', 'authors': ['Доусон Майкл'], 'price': [None, 1087, 1393], 'rating': 9.13}
{'_id': ObjectId('61ba44b4eda375952c96639b'), 'name': 'Учим Python, делая крутые игры', 'link': 'https://www.labirint.ru/books/644956/', 'authors': ['Свейгарт Эл'], 'price': [None, 757, 971], 'rating': 9.45}
{'_id': ObjectId('61ba44b4eda375952c96639c'), 'name': 'Программируем с детьми. Создайте 50 крутых игр на Python', 'link': 'https://www.labirint.ru/books/822025/', 'authors': ['Таке Адриана'], 'price': [None, 969, 1242], 'rating': 4.5}
{'_id': ObjectId('61ba44b4eda375952c96639d'), 'name': 'Python. Быстрый старт', 'link': 'https://www.labirint.ru/books/793071/', 'authors': ['Чан Джейми'], 'price': [None, 808, 1036], 'rating': 0.0}
{'_id': ObjectId('61ba44b4eda375952c96639e'), 'name': 'Python и наука о данных для чайников', 'link': 'https://www.labirint.ru/books/764415/', 'authors': ['Мюллер Джон Пол', 'Массарон Лука'], 'price': [None, 1619, 2075], 'rating': 7.0}
{'_id': ObjectId('61ba44b4eda375952c96639f'), 'name': 'Изучаем Python. Программирование игр, визуализация данных, веб-приложения', 'link': 'https://www.labirint.ru/books/733470/', 'authors': ['Мэтиз Эрик'], 'price': [None, 1304, 1672], 'rating': 9.0}
{'_id': ObjectId('61ba44b4eda375952c9663a0'), 'name': 'Python, например', 'link': 'https://www.labirint.ru/books/812753/', 'authors': ['Лейси Никола'], 'price': [None, 987, 1265], 'rating': 9.0}
{'_id': ObjectId('61ba44b4eda375952c9663a1'), 'name': 'Начинаем программировать на Python', 'link': 'https://www.labirint.ru/books/663312/', 'authors': ['Гэддис Тони'], 'price': [None, 1628, 2087], 'rating': 9.78}
{'_id': ObjectId('61ba44b4eda375952c9663a2'), 'name': 'Паттерны разработки на Python. TDD, DDD и событийно-ориентированная архитектура', 'link': 'https://www.labirint.ru/books/830329/', 'authors': ['Персиваль Гарри', 'Грегори Боб'], 'price': [None, 1682, 2157], 'rating': 0.0}
{'_id': ObjectId('61ba44b4eda375952c9663a3'), 'name': 'Python. Сборник упражнений', 'link': 'https://www.labirint.ru/books/789308/', 'authors': ['Стивенсон Бен'], 'price': [None, 1097, 1407], 'rating': 10.0}
{'_id': ObjectId('61ba44b4eda375952c9663a4'), 'name': 'Python для всех', 'link': 'https://www.labirint.ru/books/834613/', 'authors': ['Северанс Чарльз Р.'], 'price': [None, 1016, 1302], 'rating': 0.0}
{'_id': ObjectId('61ba44b4eda375952c9663a5'), 'name': 'Python на практике', 'link': 'https://www.labirint.ru/books/435407/', 'authors': ['Саммерфилд Марк'], 'price': [None, 1097, 1407], 'rating': 8.5}
{'_id': ObjectId('61ba44b4eda375952c9663a6'), 'name': 'Python. Экспресс-курс', 'link': 'https://www.labirint.ru/books/672736/', 'authors': ['Седер Наоми'], 'price': [None, 1155, 1481], 'rating': 9.33}
{'_id': ObjectId('61ba44b4eda375952c9663a7'), 'name': 'Python. Лучшие практики и инструменты', 'link': 'https://www.labirint.ru/books/802158/', 'authors': ['Яворски Михаил', 'Зиаде Терек'], 'price': [None, 2210, 2833], 'rating': 0.0}
{'_id': ObjectId('61ba44b5eda375952c9663a8'), 'name': 'Python. Справочник. Полное описание языка', 'link': 'https://www.labirint.ru/books/667550/', 'authors': ['Мартелли Алекс', 'Холден Стив', 'Рейвенскрофт Анна'], 'price': [None, 3371, 4322], 'rating': 10.0}
{'_id': ObjectId('61ba44b5eda375952c9663a9'), 'name': 'Python. Карманный справочник', 'link': 'https://www.labirint.ru/books/512926/', 'authors': ['Лутц Марк'], 'price': [None, 1080, 1384], 'rating': 8.62}
{'_id': ObjectId('61ba44b5eda375952c9663aa'), 'name': 'Python для детей', 'link': 'https://www.labirint.ru/books/700999/', 'authors': ['Шуманн Ханс-Георг'], 'price': [None, 1463, 1876], 'rating': 9.0}
{'_id': ObjectId('61ba44b5eda375952c9663ab'), 'name': 'Python для чайников', 'link': 'https://www.labirint.ru/books/703167/', 'authors': ['Мюллер Джон Пол'], 'price': [None, 1619, 2075], 'rating': 8.0}
{'_id': ObjectId('61ba44b5eda375952c9663ac'), 'name': 'Python. Книга Рецептов', 'link': 'https://www.labirint.ru/books/708689/', 'authors': ['Бизли Дэвид', 'Джонс Брайан К.'], 'price': [None, 2927, 3752], 'rating': 9.6}
{'_id': ObjectId('61ba44b5eda375952c9663ad'), 'name': 'Python. Разработка на основе тестирования', 'link': 'https://www.labirint.ru/books/641696/', 'authors': ['Персиваль Гарри'], 'price': [None, 2743, 3517], 'rating': 7.75}
{'_id': ObjectId('61ba44b5eda375952c9663ae'), 'name': 'Python для сложных задач. Наука о данных и машинное обучение', 'link': 'https://www.labirint.ru/books/609684/', 'authors': ['Плас Дж. Вандер'], 'price': [None, 1513, 1940], 'rating': 6.24}
{'_id': ObjectId('61ba44b5eda375952c9663af'), 'name': 'Python и анализ данных', 'link': 'https://www.labirint.ru/books/718860/', 'authors': ['Маккини Уэс'], 'price': [None, 2377, 3048], 'rating': 6.25}
{'_id': ObjectId('61ba44b5eda375952c9663b0'), 'name': 'Python. Искусственный интеллект, большие данные и облачные вычисления', 'link': 'https://www.labirint.ru/books/751513/', 'authors': ['Дейтел Пол Дж.', 'Дейтел Харви'], 'price': [None, 2715, 3481], 'rating': 3.9}
{'_id': ObjectId('61ba44b5eda375952c9663b1'), 'name': 'Python. К вершинам мастерства', 'link': 'https://www.labirint.ru/books/516656/', 'authors': ['Рамальо Лучано'], 'price': [None, 1829, 2345], 'rating': 7.94}
{'_id': ObjectId('61ba44b5eda375952c9663b2'), 'name': 'Python и машинное обучение. Машинное и глубокое обучение с использованием Python, scikit-learn', 'link': 'https://www.labirint.ru/books/772920/', 'authors': ['Рашка Себастьян', 'Мирджалили Вахид'], 'price': [None, 4045, 5186], 'rating': 4.0}
{'_id': ObjectId('61ba44b5eda375952c9663b3'), 'name': 'Python для детей. Самоучитель по программированию', 'link': 'https://www.labirint.ru/books/575392/', 'authors': ['Бриггс Джейсон'], 'price': [None, 1124, 1441], 'rating': 9.03}
"""