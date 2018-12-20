"""import scrapy module"""
import time
import scrapy
from scrapy.linkextractors import LinkExtractor
from elasticScrapy.items import ElasticscrapyItem
from elasticScrapy.itemloders import ElasticItemLoader

class ElasticSpider(scrapy.Spider):
    """Test Scrapy + ElasticSearch"""
    name = 'elastic'
    start_urls = ['https://www.tutorialspoint.com/tutorialslibrary.htm']
    def start_requests(self):
        """Method which starts the requests by visiting all URLs specified in start_urls"""
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        """Parse response and load to item."""
        items = []
        entries = LinkExtractor(
            restrict_xpaths='//div[@class="row featured-boxes"]',
            canonicalize=True, unique=True).extract_links(response)

        for entry in entries:
            #print(response.urljoin(entry.url))
            request = scrapy.Request(
                response.urljoin(entry.url),
                callback=self.doc_parse)
            items.append(request)

        return items

    def doc_parse(self, response):
        """Parse response and load to item."""
        items = []
        links = LinkExtractor(
            restrict_xpaths='//aside/ul[@class="nav nav-list primary left-menu"]',
            canonicalize=True, unique=True).extract_links(response)
        # Load doc homepage
        start = 8 if response.url.startswith('https') else 7
        doc = ElasticItemLoader(item=ElasticscrapyItem(), response=response)
        doc.add_value('url', response.url[start:])
        doc.add_value('canonicalId', "www.tutorialspoint.com/"+response.url.split("/")[3])
        doc.add_xpath('title', '//title/text()')
        doc.add_xpath('sectionTitles', '//h1/text() | //h2/text() | //h3/text()')
        doc.add_xpath('content', '//div[@class="content"]/div//p/text() | //b/text()')
        doc.add_value('pageNumber', 1)
        doc.add_value('lastUpdated', time.time())
        items.append(doc.load_item())
        for index, link in enumerate(links):
            request = scrapy.Request(
                response.urljoin(link.url),
                callback=self.page_parse)
            request.meta['page'] = index + 1
            items.append(request)
        return items

    def page_parse(self, response):
        """Locd every page item"""
        start = 8 if response.url.startswith('https') else 7
        doc = ElasticItemLoader(item=ElasticscrapyItem(), response=response)
        doc.add_value('url', response.url[start:])
        doc.add_value('canonicalId', "www.tutorialspoint.com/"+response.url.split("/")[3])
        doc.add_xpath('title', '//title/text()')
        doc.add_xpath('sectionTitles', '//h1/text() | //h2/text() | //h3/text()')
        doc.add_xpath('content', '//div[@class="content"]/div//p/text() | //b/text()')
        doc.add_value('pageNumber', response.meta['page'])
        doc.add_value('lastUpdated', time.time())
        return doc.load_item()
        