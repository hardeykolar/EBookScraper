# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class BookextractorItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_link = Field()
    title = Field()
    price = Field()
    availability = Field()
    star = Field()
    upc = Field()

    
