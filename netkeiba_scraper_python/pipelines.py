# -*- coding: utf-8 -*-

import logging

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
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        if spider.name == 'jockey':
            self.process_item_jockey(item)
        elif spider.name == 'horse':
            self.process_item_horse(item)
        elif spider.name == 'race':
            self.process_item_race(item)
        elif spider.name == 'racehorse':
            self.process_item_racehorse(item)
        elif spider.name == 'raceresult':
            self.process_item_raceresult(item)
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
        try:
            self.session.add(race)
            self.session.commit()
        except Exception as e:
            self.logger.error(e)

    def process_item_racehorse(self, item):
        racehorse = model.RaceHorse()
        racehorse.race_id = item['race_id']
        racehorse.goal_rank = item['goal_rank']
        racehorse.frame_number = item['frame_number']
        racehorse.horse_number = item['horse_number']
        racehorse.horse_id = item['horse_id']
        racehorse.jockey_id = item['jockey_id']
        racehorse.time = item['time']
        racehorse.agari = item['agari']
        racehorse.tansyo_odds = item['tansyo_odds']
        racehorse.popular_rank = item['popular_rank']
        racehorse.horse_weight = item['horse_weight']
        racehorse.sex_age = item['sex_age']
        racehorse.burden_weight = item['burden_weight']
        racehorse.netkeiba_url = item['netkeiba_url']

        self.session.add(racehorse)
        self.session.commit()

    def process_item_raceresult(self, item):
        raceresult = model.RaceResult()
        raceresult.race_id = item['race_id']
        raceresult.netkeiba_url = item['netkeiba_url']
        raceresult.odds_tansyo = item['odds_tansyo']
        raceresult.odds_hukusyo_1 = item['odds_hukusyo_1']
        raceresult.odds_hukusyo_2 = item['odds_hukusyo_2']
        raceresult.odds_hukusyo_3 = item['odds_hukusyo_3']
        raceresult.odds_wakuren = item['odds_wakuren']
        raceresult.odds_umaren = item['odds_umaren']
        raceresult.odds_wide_1 = item['odds_wide_1']
        raceresult.odds_wide_2 = item['odds_wide_2']
        raceresult.odds_wide_3 = item['odds_wide_3']
        raceresult.odds_umatan = item['odds_umatan']
        raceresult.odds_sanrenpuku = item['odds_sanrenpuku']
        raceresult.odds_sanrentan = item['odds_sanrentan']
        raceresult.combi_tansyo = item['combi_tansyo']
        raceresult.combi_hukusyo_1 = item['combi_hukusyo_1']
        raceresult.combi_hukusyo_2 = item['combi_hukusyo_2']
        raceresult.combi_hukusyo_3 = item['combi_hukusyo_3']
        raceresult.combi_wakuren = item['combi_wakuren']
        raceresult.combi_umaren = item['combi_umaren']
        raceresult.combi_wide_1 = item['combi_wide_1']
        raceresult.combi_wide_2 = item['combi_wide_2']
        raceresult.combi_wide_3 = item['combi_wide_3']
        raceresult.combi_umatan = item['combi_umatan']
        raceresult.combi_sanrenpuku = item['combi_sanrenpuku']
        raceresult.combi_sanrentan = item['combi_sanrentan']

        self.session.add(raceresult)
        self.session.commit()

