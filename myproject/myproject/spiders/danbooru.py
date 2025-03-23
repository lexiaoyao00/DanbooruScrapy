import scrapy
from scrapy import Selector
from myproject.items import DanbooruItem


class DanbooruSpider(scrapy.Spider):
    name = "danbooru"
    allowed_domains = ["danbooru.donmai.us"]
    start_urls = ["https://danbooru.donmai.us"]
    custom_settings = {
        "ITEM_PIPELINES": {"myproject.pipelines.DynamicJsonWriterPipeline": 300},
    }

    def parse(self, response):
        sel = Selector(response)
        list_items = sel.css('div.posts-container article')

        for item in list_items:
            post_item = DanbooruItem()
            id = item.css('article::attr(data-id)').extract_first()
            post_url = item.css('a.post-preview-link::attr(href)').extract_first()
            pre_img = item.css('a.post-preview-link picture img::attr(src)').extract_first()

            post_item['id'] = id
            post_item['post_url'] = post_url
            post_item['preview_img'] = pre_img

            yield post_item
