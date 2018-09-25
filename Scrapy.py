from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field

class Item(Item):
    url= Field() #find all image urls in a web page 
    href= Field() #find all hyperlinks in a web page
    
class Spider(CrawlSpider):
    name = 'fox.com'
    allowed_domains = ['fox.com']
    start_urls = ['https://www.fox.com/']
    rules = (
        Rule(LinkExtractor(), callback='parse_item'), # Extract Links
    )

    def parse_item(self, response):
        item = Item()
        item['url'] = []
        item['href'] = []
        for link in LinkExtractor(allow=()).extract_links(response):
            for imageurl in response.xpath('//img/@src').extract():
                item['url'].append(response.urljoin(imageurl))
            for link in response.xpath('//a/@href').extract():
                item['href'].append(response.urljoin(link))
            return item

#Run Scrapy from script   
process = CrawlerProcess(get_project_settings())
process.crawl(Spider)
process.start() 
