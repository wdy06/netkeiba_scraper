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


class Race(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    race_number = scrapy.Field()
    plain_obstacle = scrapy.Field()
    course_field = scrapy.Field()
    leftright = scrapy.Field()
    distance = scrapy.Field()
    age_condition = scrapy.Field()
    race_grade = scrapy.Field()
    racetrack = scrapy.Field()
    entry_restrict = scrapy.Field()
    weight_condition = scrapy.Field()
    entry_count = scrapy.Field()
    weather = scrapy.Field()
    track_condition = scrapy.Field()
    netkeiba_url = scrapy.Field()


class RaceHorse(scrapy.Item):
    race_id = scrapy.Field()
    goal_rank = scrapy.Field()
    frame_number = scrapy.Field()
    horse_number = scrapy.Field()
    horse_id = scrapy.Field()
    jockey_id = scrapy.Field()
    time = scrapy.Field()
    agari = scrapy.Field()
    tansyo_odds = scrapy.Field()
    popular_rank = scrapy.Field()
    horse_weight = scrapy.Field()
    sex_age = scrapy.Field()
    burden_weight = scrapy.Field()
    netkeiba_url = scrapy.Field()


class RaceResult(scrapy.Item):
    race_id = scrapy.Field()
    odds_tansyo = scrapy.Field()
    odds_hukusyo = scrapy.Field()
    odds_wakuren = scrapy.Field()
    odds_umaren = scrapy.Field()
    odds_wide = scrapy.Field()
    odds_umatan = scrapy.Field()
    odds_sanrenpuku = scrapy.Field()
    odds_sanrentan = scrapy.Field()
    combi_tansyo = scrapy.Field()
    combi_hukusyo = scrapy.Field()
    combi_wakuren = scrapy.Field()
    combi_umaren = scrapy.Field()
    combi_wide = scrapy.Field()
    combi_umatan = scrapy.Field()
    combi_sanrenpuku = scrapy.Field()
    combi_sanrenpuku = scrapy.Field()
