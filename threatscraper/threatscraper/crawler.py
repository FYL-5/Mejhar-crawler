from threatscraper.spiders.AzSpider import AzSpider
from threatscraper.spiders.CCNSpider import CCNSpider
from threatscraper.spiders.JpSpider import JpSpider
from threatscraper.spiders.KoreaSpider import KoreaSpider
from threatscraper.spiders.threatscraper import SaSpider

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(AzSpider)
    process.crawl(CCNSpider)
    process.crawl(JpSpider)
    process.crawl(KoreaSpider)
    process.crawl(SaSpider)
    process.start()


if __name__ == '__main__':
    main()