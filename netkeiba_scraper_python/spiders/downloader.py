import os

import scrapy

from .. import util


class DownloaderSpider(scrapy.Spider):
    name = 'downloader'

    start_urls = util.load_url_list(
        './netkeiba_scraper_python/spiders/data/race_url_list.txt')
    start_urls.extend(util.load_url_list(
        './netkeiba_scraper_python/spiders/data/jockey_url_list.txt'))
    start_urls.extend(util.load_url_list(
        './netkeiba_scraper_python/spiders/data/horse_url_list.txt'))

    def __init__(self):
        self.url = None
        self.text = None
        self.HTML_DIR_JOCKEY = './netkeiba_scraper_python/spiders/data/html/jockey'
        self.HTML_DIR_HORCE = './netkeiba_scraper_python/spiders/data/html/horse'
        self.HTML_DIR_RACE = './netkeiba_scraper_python/spiders/data/html/race'
        if not os.path.exists(self.HTML_DIR_JOCKEY):
            os.makedirs(self.HTML_DIR_JOCKEY)
        if not os.path.exists(self.HTML_DIR_HORCE):
            os.makedirs(self.HTML_DIR_HORCE)
        if not os.path.exists(self.HTML_DIR_RACE):
            os.makedirs(self.HTML_DIR_RACE)

    def parse(self, response):
        self.url = response.url
        self.text = response.text
        self.save_html_file()

    def save_html_file(self):
        if 'jockey' in self.url:
            url_id = util.jockey_profile_url2id(self.url)
            file_path = os.path.join(self.HTML_DIR_JOCKEY, url_id)
        elif 'horse' in self.url:
            url_id = util.horse_profile_url2id(self.url)
            file_path = os.path.join(self.HTML_DIR_HORCE, url_id)
        elif 'race' in self.url:
            url_id = util.race_url2id(self.url)
            file_path = os.path.join(self.HTML_DIR_RACE, url_id)
        else:
            raise Exception('unknown url format')

        with open(file_path, 'w', encoding='euc-jp') as f:
            f.write(self.text)
