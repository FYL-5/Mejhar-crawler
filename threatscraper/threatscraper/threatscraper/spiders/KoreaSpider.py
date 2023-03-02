import scrapy

from threatscraper.items import ThreatItem
from scrapy.loader import ItemLoader

class KoreaSpider(scrapy.Spider):
    name = 'KoreaCert'
    start_urls = ['https://www.korea-certification.com/en/news/']
    prefix_url = 'https://www.cert.gov.az'
    startpage=0

    def parse(self, response):
        for link in response.css('div.list_item a::attr(href)'):
            yield response.follow( link.get(), callback = self.parseSingleThreat)
 

    def parseSingleThreat(self, response):
        itemLoader = ItemLoader(item= ThreatItem(), selector= response)  
        itemLoader.add_css('name', 'h1.pagetitle.post::text')
        itemLoader.add_css('date', 'div.post_date::text')
        itemLoader.add_css('description','#content_wrap p::text')
        itemLoader.add_xpath('url','/html/head/meta[5]/@content')

       
        yield itemLoader.load_item()