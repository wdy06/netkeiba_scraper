import re

import scrapy

from ..items import RaceHorse
from .. import util
from . import race


class RaceHorseSpider(scrapy.Spider):
    name = 'racehorse'
    start_urls = util.load_url_list('./netkeiba_scraper_python/spiders/data/race_url_list.txt')

    def parse(self, response):
        table = response.css('#contents_liquid > table')
        for i, line in enumerate(table.css('tr')):
            if i == 0:
                continue
            item = self.table_line_parser(line)
        item['race_id'] = race.race_url2id(response.url)
        item['netkeiba_url'] = response.url
        yield item

    def table_line_parser(self, line_selector):
        item = RaceHorse()
        cells = line_selector.css('td')
        item['goal_rank'] = int(cells[0].css('::text').extract_first())
        item['frame_number'] = int(cells[1].css('span::text').extract_first())
        item['horse_number'] = int(cells[2].css('::text').extract_first())
        horse_id_text = cells[3].css('a::attr(href)').extract_first()
        item['horse_id'] = self.process_horse_id_text(horse_id_text)
        item['sex_age'] = cells[4].css('::text').extract_first()
        item['burden_weight'] = int(cells[5].css('::text').extract_first())
        jockey_id_text = cells[6].css('a::attr(href)').extract_first()
        item['jockey_id'] = self.process_jockey_id_text(jockey_id_text)
        time_text = cells[7].css('::text').extract_first()
        item['time'] = self.process_time_text(time_text)
        item['agari'] = float(cells[11].css('::text').extract_first())
        item['tansyo_odds'] = float(cells[12].css('::text').extract_first())
        item['popular_rank'] = int(cells[13].css('::text').extract_first())
        horse_weight_text = cells[14].css('::text').extract_first()
        item['horse_weight'] = self.process_horse_weight(horse_weight_text)

        return item

    def process_horse_id_text(self, text):
        text = text.replace('horse', '')
        return int(text.replace('/', ''))

    def process_jockey_id_text(self, text):
        text = text.replace('jockey', '')
        return text.replace('/', '')

    def process_time_text(self, text):
        minites = float(text[:text.find(':')])
        seconds = float(text[text.find(':') + 1:])
        return minites * 60 + seconds

    def process_horse_weight(self, text):
        return int(re.sub('\(.*\)', '', text))
