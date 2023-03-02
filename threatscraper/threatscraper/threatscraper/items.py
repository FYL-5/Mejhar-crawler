# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose,Join
from w3lib.html import remove_tags

def replaceBullet (input):
    return input.replace('\u25cf','').strip()

def replaceNewLine (input):
    return input.replace('\n','').replace('\t', '').strip()

def replaceMultiSpace (input):
    return re.sub('\s+',' ',input)
    
#name = scrapy.Field( input_processor= MapCompose(remove_tags), out_processor = TakeFirst())
class ThreatItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor = MapCompose(remove_tags, replaceNewLine), output_processor = TakeFirst())
    date = scrapy.Field(input_processor = MapCompose(remove_tags, replaceNewLine), output_processor = TakeFirst())
    severity_level = scrapy.Field(input_processor = MapCompose(remove_tags,replaceBullet, replaceNewLine ), output_processor = TakeFirst())
    warning_number = scrapy.Field(input_processor = MapCompose(remove_tags, replaceNewLine), output_processor = TakeFirst())
    target_sector = scrapy.Field(input_processor = MapCompose(remove_tags, replaceNewLine), output_processor = TakeFirst())
    description = scrapy.Field(input_processor = MapCompose(remove_tags, replaceNewLine,replaceMultiSpace), output_processor = Join(' '))
    url = scrapy.Field(input_processor = MapCompose(remove_tags, replaceNewLine), output_processor = TakeFirst())

