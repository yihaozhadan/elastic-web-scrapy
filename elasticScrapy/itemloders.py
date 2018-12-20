"""Define the processing logic when load item in and out"""
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose

def filter_blank(value):
    """Filter out string which lenght is less than 2"""
    return None if len(value.strip()) < 2 else value

class ElasticItemLoader(ItemLoader):
    """Define the processing logic when load item in and out"""
    url_out = TakeFirst()
    title_out = TakeFirst()
    canonicalId_out = TakeFirst()
    sectionTitles_in = MapCompose(filter_blank)
    content_in = MapCompose(filter_blank)
    pageNumber_out = TakeFirst()
    lastUpdated_out = TakeFirst()
    