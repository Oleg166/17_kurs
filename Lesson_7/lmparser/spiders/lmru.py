import scrapy
from scrapy.http import HtmlResponse
from lmparser.items import LmParserItem
from scrapy.loader import ItemLoader


class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response):
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//div[@class="phytpj4_plp largeCard"]/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.item_parse)

    def item_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LmParserItem(), selector=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('pictures', '//picture[@slot="pictures"]/source/@srcset')
        yield loader.load_item()

# пример сохраненных данных в базе:
"""
{'_id': ObjectId('61bce4315cde551c55f7e895'), 
 'name': 'Киянка Dexter 450 г резиновая, деревянная ручка, цвет черный', 
 'price': 337, 
 'url': 'https://leroymerlin.ru/product/kiyanka-dexter-450-g-rezinovaya-81968469/', 
 'pictures': [{'url': 'https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/81968469.jpg', 
               'path': 'full/6b7ecde4db4ca1a2b0b6df9e48aa9c4d69ce2936.jpg', 
               'checksum': 'a63968583d8a4e8d57cc46a79d4c48f1', 
               'status': 'uptodate'}, 
              {'url': 'https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/81968469_01.jpg', 
               'path': 'full/6d5feddc9417dcfc58271102a4e578f54627e40a.jpg', 
               'checksum': 'd99581a7270ac0892adc9dc69332312d', 
               'status': 'uptodate'}]}
{'_id': ObjectId('61bce4335cde551c55f7e896'), 
 'name': 'Молоток TRUPER столярный фиберглассовая ручка 0,45 кг MAR-16F 19997', 
 'price': 1190, 
 'url': 'https://leroymerlin.ru/product/molotok-truper-stolyarnyy-fiberglassovaya-ruchka-0-90170982/', 
 'pictures': [{'url': 'https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/90170982.jpg', 
               'path': 'full/8865109984406c5561fb682fa057d8fc9e4d84e2.jpg', 
               'checksum': '09b17dbcf3439dfa2cb41af4655cb365', 
               'status': 'uptodate'}]}
{'_id': ObjectId('61bce4355cde551c55f7e897'), 
 'name': 'Молоток слесарный 100 г деревянная ручка', 
 'price': 120, 
 'url': 'https://leroymerlin.ru/product/molotok-slesarnyy-100-g-derevyannaya-ruchka-82116375/', 
 'pictures': [{'url': 'https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82116375.jpg', 
               'path': 'full/7e41f20dd9ae7eacae2e6f8172d0a73e4fbfad15.jpg', 
               'checksum': 'f3319435778700a5ea6c4a84352fc166', 
               'status': 'downloaded'}, 
              {'url': 'https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82116375_01.jpg', 
               'path': 'full/6b303956316052d4db57cd36f6a9cb63f2297d07.jpg', 
               'checksum': 'af978081c27690f849d4c2fdae516746', 
               'status': 'downloaded'}, 
              {'url': 'https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82116375_02.jpg', 
               'path': 'full/6728803b159561c4c07b269bb672c068d0cc4b9f.jpg', 
               'checksum': 'c3dc69d0a6d4dc52b932584ed0739430', 
               'status': 'downloaded'}, 
              {'url': 'https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82116375_03.jpg', 
               'path': 'full/d83a9c9e09ca04f3e5565a80e3724ca49ef01bdc.jpg', 
               'checksum': '108c4d30cb7383665bb5124bb67c4730', 
               'status': 'downloaded'}, 
              {'url': 'https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82116375_04.jpg', 
               'path': 'full/4ce5f9f926a146af56e5e3fb92a42387487d7ea6.jpg', 
               'checksum': '704f1f9bcb3b952f39a296952ebd7d2a', 
               'status': 'downloaded'}, 
              {'url': 'https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82116375_05.jpg', 
               'path': 'full/8dfc86de6b708bb54292d18e139670a3d092e25d.jpg', 
               'checksum': 'fc5978eaae036e45f7e252f7091dca54', 
               'status': 'downloaded'}]}
"""