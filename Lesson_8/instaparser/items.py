# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    username_main = scrapy.Field()
    usertype = scrapy.Field()
    username = scrapy.Field()
    id_user = scrapy.Field()
    userphoto = scrapy.Field()
    _id = scrapy.Field()
