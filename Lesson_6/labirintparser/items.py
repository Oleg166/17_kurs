# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LabirintparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    _id = scrapy.Field()
    authors = scrapy.Field()
    price = scrapy.Field()
    # price_discount = scrapy.Field()
    rating = scrapy.Field()
