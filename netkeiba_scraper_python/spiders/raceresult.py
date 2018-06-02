import re

import scrapy

from ..items import RaceResult
from .. import util
from . import race


class RaceResultSpider(scrapy.Spider):
    name = 'raceresult'
    start_urls = util.load_url_list('./netkeiba_scraper_python/spiders/data/race_url_list.txt')

    def parse(self, response):
        item = RaceResult()
        item = self.init_item(item)
        item['race_id'] = race.race_url2id(response.url)
        item['netkeiba_url'] = response.url

        table_lines = response.css('div.result_info.box_left > diary_snap table').css('tr')
        result_list = table_lines.css('th::text').extract()
        for i, result_name in enumerate(result_list):
            if result_name == u'単勝':
                tansyo_line = table_lines[i].css('td::text').extract()
                item['combi_tansyo'] = tansyo_line[0]
                item['odds_tansyo'] = self.process_odds_text(tansyo_line[1])

            if result_name == u'複勝':
                hukusyo_line = table_lines[i].css('td::text').extract()
                item['combi_hukusyo_1'] = hukusyo_line[0]
                item['combi_hukusyo_2'] = hukusyo_line[1]
                item['combi_hukusyo_3'] = hukusyo_line[2]
                item['odds_hukusyo_1'] = self.process_odds_text(hukusyo_line[3])
                item['odds_hukusyo_2'] = self.process_odds_text(hukusyo_line[4])
                item['odds_hukusyo_3'] = self.process_odds_text(hukusyo_line[5])

            if result_name == u'枠連':
                wakuren_line = table_lines[i].css('td::text').extract()
                item['combi_wakuren'] = wakuren_line[0]
                item['odds_wakuren'] = self.process_odds_text(wakuren_line[1])

            if result_name == u'馬連':
                umaren_line = table_lines[i].css('td::text').extract()
                item['combi_umaren'] = umaren_line[0]
                item['odds_umaren'] = self.process_odds_text(umaren_line[1])

            if result_name == u'ワイド':
                wide_line = table_lines[i].css('td::text').extract()
                item['combi_wide_1'] = wide_line[0]
                item['combi_wide_2'] = wide_line[1]
                item['combi_wide_3'] = wide_line[2]
                item['odds_wide_1'] = self.process_odds_text(wide_line[3])
                item['odds_wide_2'] = self.process_odds_text(wide_line[4])
                item['odds_wide_3'] = self.process_odds_text(wide_line[5])

            if result_name == u'馬単':
                umatan_line = table_lines[i].css('td::text').extract()
                item['combi_umatan'] = umatan_line[0]
                item['odds_umatan'] = self.process_odds_text(umatan_line[1])

            if result_name == u'三連複':
                sanrenpuku_line = table_lines[i].css('td::text').extract()
                item['combi_sanrenpuku'] = sanrenpuku_line[0]
                item['odds_sanrenpuku'] = self.process_odds_text(sanrenpuku_line[1])

            if result_name == u'三連単':
                sanrentan_line = table_lines[i].css('td::text').extract()
                item['combi_sanrentan'] = sanrentan_line[0]
                item['odds_sanrentan'] = self.process_odds_text(sanrentan_line[1])

        yield item

    def init_item(self, item):
        for element in item.fields:
            item[element] = None
        return item

    def process_odds_text(self, text):
        return int(text.replace(',', ''))
