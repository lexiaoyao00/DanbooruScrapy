import scrapy


class DanbooruSpider(scrapy.Spider):
    name = "danbooru"
    allowed_domains = ["danbooru.donmai.us"]
    start_urls = ["https://danbooru.donmai.us"]

    def parse(self, response):
        pass
