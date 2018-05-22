# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NetkeibaScraperPythonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Jockey(scrapy.Item):

    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()


class Horse(scrapy.Item):

    id = scrapy.Field()
    name = scrapy.Field()
    birthdate = scrapy.Field()
    winnings_prize = scrapy.Field()
    trainer = scrapy.Field()
    url = scrapy.Field()
