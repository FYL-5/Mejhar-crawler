import scrapy

from threatscraper.items import ThreatItem
from scrapy.loader import ItemLoader

#not working
class JpSpider(scrapy.Spider):
    name = 'JpCert'
    start_urls = ['https://www.jpcert.or.jp/english/at/2023.html']
    prefix_url = 'https://www.jpcert.or.jp/english/at/'
    event_prefix = 'https://www.jpcert.or.jp'
 

    def parse(self, response):
        for link in response.css('ul.history_list.cf a::attr(href)'):
            yield response.follow(self.prefix_url + link.get(), callback = self.parseyear)


    def parseyear(self, response):
        for link in response.css('td.event_detail a::attr(href)'):
            yield response.follow(self.event_prefix + link.get(), callback = self.parseSingleThreat)

    def parseSingleThreat(self, response):
        itemLoader = ItemLoader(item= ThreatItem(), selector= response)  
        itemLoader.add_css('name', 'div.page_title_area h3::text')
        itemLoader.add_xpath('date', '//*[@id="link_pgtop"]/div/div[2]/article/div/text()[1]')
        itemLoader.add_css('description','article ::text')
        itemLoader.add_xpath('url','/html/head/meta[7]/@content')
        yield itemLoader.load_item()