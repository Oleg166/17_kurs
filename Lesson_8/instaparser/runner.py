from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instaparser import settings
from instaparser.spiders.instacom import InstacomSpider

users = ['d_k_solution', 'aminqahramanii']

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    for j in users:
        process.crawl(InstacomSpider, user=j)

    process.start()
