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
        elif spider.name == 'race':
            self.process_item_race(item)
        return item

    def open_spider(self, spider):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        model.Base.metadata.create_all(bind=self.engine)

    def close_spider(self, spider):
        self.session.close()

    def process_item_jockey(self, item):
        jockey = model.Jockey()
        jockey.id = item['id']
        jockey.name = item['name']
        jockey.url = item['url']
        self.session.add(jockey)
        self.session.commit()

    def process_item_horse(self, item):
        horse = model.Horse()
        horse.id = item['id']
        horse.name = item['name']
        horse.birthdate = item['birthdate']
        horse.winnings_prize = item['winnings_prize']
        horse.trainer = item['trainer']
        horse.url = item['url']
        self.session.add(horse)
        self.session.commit()

    def process_item_race(self, item):
        race = model.Race()
        race.id = item['id']
        race.name = item['name']
        race.date = item['date']
        race.race_number = item['race_number']
        race.plain_obstacle = item['plain_obstacle']
        race.course_field = item['course_field']
        race.leftright = item['leftright']
        race.distance = item['distance']
        race.age_condition = item['age_condition']
        race.race_grade = item['race_grade']
        race.racetrack = item['racetrack']
        race.entry_restrict = item['entry_restrict']
        race.weight_condition = item['weight_condition']
        race.entry_count = item['entry_count']
        race.weather = item['weather']
        race.track_condition = item['track_condition']
        race.netkeiba_url = item['netkeiba_url']
        self.session.add(race)
        self.session.commit()
