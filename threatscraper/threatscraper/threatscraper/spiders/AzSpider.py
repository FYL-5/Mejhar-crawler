import scrapy

from threatscraper.items import ThreatItem
from scrapy.loader import ItemLoader

class AzSpider(scrapy.Spider):
    name = 'AzCert'
    start_urls = ['https://www.cert.gov.az/en/news']
    prefix_url = 'https://www.cert.gov.az'
    startpage=0

    def parse(self, response):
        for link in response.css('div.col-md-6 a::attr(href)'):
            yield response.follow(self.prefix_url + link.get(), callback = self.parseSingleThreat)

        
        next_page = response.xpath('//*[@id="pagination"]/ul/li[4]/a/@href').get()
        if self.startpage > 0:
            next_page = response.xpath('//*[@id="pagination"]/ul/li[7]/a/@href').get()
        if next_page is not None:
            yield response.follow(self.prefix_url+next_page, callback = self.parse)
        self.startpage = self.startpage+1

    def parseSingleThreat(self, response):
        itemLoader = ItemLoader(item= ThreatItem(), selector= response)  
        itemLoader.add_css('name', 'div.main-block-info.inner.news-inner div h1::text')
        itemLoader.add_css('date', 'div.time strong::text')
        itemLoader.add_xpath('description','/html/body/div[3]/div/div/div[1]')
        itemLoader.add_xpath('url','/html/head/meta[10]/@content')

       
        yield itemLoader.load_item()