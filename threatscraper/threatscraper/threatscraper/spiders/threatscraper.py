import scrapy

from threatscraper.items import ThreatItem
from scrapy.loader import ItemLoader

class SaSpider(scrapy.Spider):
    name = 'SaCert'
    start_urls = ['https://cert.gov.sa/en/security-warnings/']
    prefix_url = 'https://cert.gov.sa'

    def parse(self, response):
        for link in response.css('div.card a::attr(href)'):
            yield response.follow(self.prefix_url + link.get(), callback = self.parseSingleThreat)

        next_page = response.css('a.page-link1::attr(href)').getall()[-2]
        if next_page is not None:
            yield response.follow(self.start_urls[0]+next_page, callback = self.parse)



    def parseSingleThreat(self, response):
        itemLoader = ItemLoader(item= ThreatItem(), selector= response)  
        itemLoader.add_css('name', 'h4.cert-title')
        itemLoader.add_xpath('date', '/html/body/main/div[2]/div[3]/div[3]/div/div[2]/div[1]/div[2]/p[1]/text()')
        itemLoader.add_xpath('severity_level', '/html/body/main/div[2]/div[3]/div[3]/div/div[2]/div[1]/div[2]/p[2]/text()')
        itemLoader.add_xpath('warning_number','/html/body/main/div[2]/div[3]/div[3]/div/div[2]/div[1]/div[2]/p[3]/text()')
        itemLoader.add_xpath('target_sector','/html/body/main/div[2]/div[3]/div[3]/div/div[2]/div[1]/div[2]/p[4]/text()')
        itemLoader.add_xpath('description','/html/body/main/div[2]/div[3]/div[3]/div/div[2]/div[2]')
        itemLoader.add_xpath('url','/html/head/meta[9]/@content')

       
        yield itemLoader.load_item()