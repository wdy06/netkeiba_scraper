import scrapy

from ..items import Horse
from .. import util


class HorseSpider(scrapy.Spider):
    name = 'horse'
    start_urls = util.load_url_list('./netkeiba_scraper_python/spiders/data/horse_url_list.txt')

    def parse(self, response):
        item = Horse()
        horse_name_text = response.css('div.horse_title h1::text').extract_first()
        horse_name = self.process_horse_name(horse_name_text)
        birthdate = response.css('div.db_prof_area_02  td')[0].css('::text').extract_first()
        trainer = response.css('div.db_prof_area_02  td')[1].css('::text').extract_first()
        for i, selector in enumerate(response.css('div.db_prof_area_02  th')):
            if selector.css('::text').extract_first() == u'獲得賞金':
                row_idx = i

        winnings_prize_text = response.css('div.db_prof_area_02  td')[row_idx].css('::text').extract_first()
        winnings_prize = self.process_winning_prize(winnings_prize_text)

        item['id'] = util.horse_profile_url2id(response.url)
        item['name'] = horse_name
        item['birthdate'] = birthdate
        item['trainer'] = trainer
        item['winnings_prize'] = winnings_prize
        item['url'] = response.url
        yield item

    def process_horse_name(self, text):
        return text[:-2]

    def process_winning_prize(self, text):
        text = text.replace('\n', '')
        text = text.replace(',', '')
        text = text[:text.find(u'円')]
        oku_yen = 0
        if u'億' in text:
            oku_yen = 10000 * int(text[:text.find(u'億')])

        man_yen = int(text[text.find(u'億') + 1:text.find(u'万')])

        return oku_yen + man_yen
