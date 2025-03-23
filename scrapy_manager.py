from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings

class ScrapyManager:
    def __init__(self):
        self.crawler_process = CrawlerProcess(get_project_settings())

    def run_spider(self, spider_class):
        self.crawler_process.crawl(spider_class)
        self.crawler_process.start()

    def run_multiple_spiders(self, spider_classes):
        for spider_class in spider_classes:
            self.crawler_process.crawl(spider_class)
        self.crawler_process.start()

    def stop_crawler(self):
        self.crawler_process.stop()

    def set_custom_settings(self, settings_dict):
        custom_settings = Settings()
        custom_settings.setdict(settings_dict)
        self.crawler_process = CrawlerProcess(custom_settings)