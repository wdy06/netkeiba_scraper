# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import model


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class DatabasePipeline(object):
    def __init__(self):
        self.engine = model.db_connect()

    def process_item(self, item, spider):
        if spider.name == 'jockey':
            self.process_item_jockey(item)
        elif spider.name == 'horse':
            self.process_item_horse(item)
        return item

    def open_spider(self, spider):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        model.Base.metadata.create_all(bind=self.engine)

    def close_spider(self, spider):
        self.session.close()

    def process_item_jockey(self, item):
        jockey = model.Jockey()
        jockey.name = item['name']
        jockey.url = item['url']
        self.session.add(jockey)
        self.session.commit()

    def process_item_horse(self, item):
        horse = model.Horse()
        horse.name = item['name']
        horse.birthdate = item['birthdate']
        horse.winnings_prize = item['winnings_prize']
        horse.trainer = item['trainer']
        horse.url = item['url']
        self.session.add(horse)
        self.session.commit()
