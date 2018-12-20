"""import scrapy module"""
import time
import scrapy
from elasticScrapy.items import ElasticscrapyItem
from elasticScrapy.itemloders import ElasticItemLoader

class OnePageSpider(scrapy.Spider):
    """Test Scrapy + ElasticSearch"""
    name = 'onepage'
    start_urls = ['https://www.tutorialspoint.com/kubernetes/index.htm']
    def start_requests(self):
        """Method which starts the requests by visiting all URLs specified in start_urls"""
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        """Parse response and load to item."""
        start = 8 if response.url.startswith('https') else 7
        doc = ElasticItemLoader(item=ElasticscrapyItem(), response=response)
        doc.add_value('url', response.url[start:])
        doc.add_value('canonicalId', "www.tutorialspoint.com/"+response.url.split("/")[3])
        doc.add_xpath('title', '//title/text()')
        doc.add_xpath('sectionTitles', '//h1/text() | //h2/text() | //h3/text()')
        doc.add_xpath('content', '//div[@class="content"]/div//p/text() | //b/text()')
        doc.add_value('lastUpdated', time.time())
        return doc.load_item()
