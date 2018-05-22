import scrapy

from ..items import Jockey
from .. import util


class JockeySpider(scrapy.Spider):
    name = 'jockey'
    start_urls = util.load_url_list('./netkeiba_scraper_python/spiders/data/jockey_url_list.txt')

    def parse(self, response):
        item = Jockey()
        jockey_text = response.css('div.db_head_name.fc > h1::text').extract_first()
        jockey_name = self.process_jockey_name(jockey_text)

        item['id'] = util.jockey_profile_url2id(response.url)
        item['name'] = jockey_name
        item['url'] = response.url
        yield item

    def process_jockey_name(self, text):
        text = text.replace('\n', '')
        return text[:text.find('\xa0')
               ]