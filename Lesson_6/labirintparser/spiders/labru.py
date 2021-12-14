import scrapy


class LabruSpider(scrapy.Spider):
    name = 'labru'
    allowed_domains = ['labirint.ru']
    start_urls = ['http://labirint.ru/']

    def parse(self, response):
        pass
