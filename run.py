from scrapy_manager import ScrapyManager
from myproject.myproject.spiders.danbooru import DanbooruSpider


if __name__ == '__main__':
    manager = ScrapyManager()
    manager.run_spider(DanbooruSpider)