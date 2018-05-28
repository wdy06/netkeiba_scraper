import re

import scrapy

from ..items import Race
from .. import util


def race_url2id(url):
    return int(re.search('\d+', url).group(0))


class RaceSpider(scrapy.Spider):
    name = 'race'
    start_urls = util.load_url_list('./netkeiba_scraper_python/spiders/data/race_url_list.txt')

    def parse(self, response):
        item = Race()
        item['id'] = race_url2id(response.url)
        item['netkeiba_url'] = response.url
        name = response.css('diary_snap > div > div > dl > dd > h1::text').extract_first()
        item['name'] = name
        item['race_grade'] = self.process_race_grade(name)
        course_info_text = response.css('diary_snap > div > div > p::text').extract_first()
        item['date'] = self.process_date_text(course_info_text)
        race_number_text = response.css('diary_snap > div > div > dl > dt::text').extract_first()
        item['race_number'] = self.process_race_number_text(race_number_text)
        item['plain_obstacle'] = self.process_plain_obstacle_text(course_info_text)
        course_condition_text = response.css('diary_snap_cut > span::text').extract_first()
        item['course_field'] = self.process_course_field(course_condition_text)
        item['leftright'] = self.process_leftright(course_condition_text)
        item['distance'] = self.process_distance(course_condition_text)
        item['weather'] = self.process_weather(course_condition_text)
        item['track_condition'] = self.process_track_condition(course_condition_text)
        item['age_condition'] = self.process_age_condition(course_info_text)
        item['racetrack'] = self.process_racetrack(course_info_text)
        item['entry_restrict'] = None
        item['weight_condition'] = None
        item['entry_count'] = None
        yield item

    def process_date_text(self, text):
        return re.search('[0-9]{4}年([1-9]|1[012])月([1-9]|[12][0-9]|3[01])日', text).group(0)

    def process_race_number_text(self, text):
        return int(re.search('\d+', text).group(0))

    def process_plain_obstacle_text(self, text):
        result = re.search('(障害)', text)
        if result is not None:
            return 'obstacle'
        else:
            return 'plain'

    def process_course_field(self, text):
        result = re.match('芝|ダ|障', text)
        if result is None:
            raise ParseError
        else:
            return result.group(0)

    def process_leftright(self, text):
        result = re.search('左|右', text)
        if result is None:
            raise ParseError
        else:
            return result.group(0)

    def process_weather(self, text):
        result = re.search('(天候 : ).', text)
        if result is None:
            raise ParseError
        else:
            return result.group(0).replace('天候 : ', '')

    def process_track_condition(self, text):
        result = re.search('(芝|(ダート) : ).', text)
        if result is None:
            raise ParseError
        else:
            return re.sub('(芝|(ダート) : )', '', result.group(0))

    def process_distance(self, text):
        result = re.search('\d+m', text)
        if result is None:
            raise ParseError
        else:
            return int(result.group(0).replace('m', ''))

    def process_age_condition(self, text):
        result = re.search('(2歳|3歳|3歳以上|4歳以上)', text)
        if result is None:
            return None
        else:
            return result.group(0)

    def process_race_grade(self, text):
        result = re.search('(G1|G2|G3|OP|1600万|1000万|500万|新馬|未勝利|未出走)', text)
        if result is None:
            return None
        else:
            return result.group(0)

    def process_racetrack(self, text):
        result = re.search('(札幌|函館|福島|新潟|東京|中山|中京|京都|阪神|小倉)', text)
        if result is None:
            return None
        else:
            return result.group(0)


class ParseError(Exception):
    pass
