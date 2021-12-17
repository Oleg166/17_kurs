# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from itemloaders.processors import MapCompose, TakeFirst
import scrapy


# убираем в цене пробел
def clear_price(value):
    value = value.replace(' ', '')
    try:
        return int(value)
    except:
        return value


# из картинок выбираем только большие, ссылка на которые содержит "w_2000"
def exclusion(picture):
    if 'w_2000' in picture:
        return picture


class LmParserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_price))
    pictures = scrapy.Field(output_processor=MapCompose(), input_processor=MapCompose(exclusion))
    _id = scrapy.Field()

