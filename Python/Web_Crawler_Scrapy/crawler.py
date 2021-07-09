from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Spider(CrawlSpider):
    name = "Crawler"
    allowed_domains = ["example.com"]  #
    start_urls = ["https://example.com/"]
    rules = [Rule(LinkExtractor(), callback='parse_item', follow=True)]  # Follow any link scrapy finds (that is allowed).

    def parse_item(self, response):
        print('Got a response from %s.' % response.url)