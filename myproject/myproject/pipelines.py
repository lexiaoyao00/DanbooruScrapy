# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os
from scrapy.utils.project import get_project_settings


class DynamicJsonWriterPipeline:
    def __init__(self):
        settings = get_project_settings()
        # 统一数据目录路径（如项目根目录下的 data 文件夹）
        self.data_dir = os.path.join(settings.get("PROJECT_ROOT"), "data")
        os.makedirs(self.data_dir, exist_ok=True)  # 自动创建目录

    def open_spider(self, spider):
        self.filename = os.path.join(
            self.data_dir,
            f"{spider.name}.json"
        )
        print(f' data file name : {self.filename}')
        self.file = open(self.filename, 'w', encoding='utf-8')
        self.file.write('[\n')
        self.first_item = True

    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)
        if self.first_item:
            self.file.write(line)
            self.first_item = False
        else:
            self.file.write(',\n' + line)
        return item

class MyprojectPipeline:
    def process_item(self, item, spider):
        return item
