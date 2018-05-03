# -*- coding: utf-8 -*-

import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


class URLCollector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(name)s %(filename)s:%(lineno)d %(message)s')

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

        self.chrome_driver_path = './python/chromedriver'


class RaceURLCollector(URLCollector):
    def get_url_list(self):

        try:
            self.logger.info("start")

            driver = webdriver.Chrome(self.chrome_driver_path, chrome_options=self.chrome_options)
            target_url = 'http://db.netkeiba.com/?pid=race_search_detail'
            driver.get(target_url)
            self.logger.info('connection success')

            driver.find_element_by_id("check_track_1").click()
            driver.find_element_by_id("check_track_2").click()
            driver.find_element_by_id("check_track_3").click()
            element = driver.find_element_by_css_selector('#db_search_detail_form > form > table >'
                                                               ' tbody > tr:nth-child(11) > td > select')
            Select(element).select_by_value('100')
            driver.find_element_by_xpath('//*[@id="db_search_detail_form"]/form/div/input[1]').submit()
            time.sleep(2)

            assert driver.find_element_by_tag_name('h2').text == u'競走種別[芝、ダート、障害]、期間[無指定～無指定]の検索結果', \
                'This is not expected page.'

            # get total race count
            pager = driver.find_element_by_id('contents_liquid').find_element_by_class_name('pager')
            pages = pager.text.replace(',', '')
            total_race_count = int(pages[:pages.find(u'件')])
            self.logger.info('total race count {}'.format(total_race_count))

            race_url_list = []
            for page_count in range(total_race_count // 100 + 1):
                pager = driver.find_element_by_id('contents_liquid').find_element_by_class_name('pager')
                pages = pager.text.replace(',', '')
                self.logger.info(pages[:pages.find(u'目')])

                race_table = driver.find_element_by_class_name('race_table_01')
                for i, race_element in enumerate(race_table.find_elements_by_tag_name('tr')):
                    if i == 0:
                        continue
                    race_name = race_element.find_elements_by_tag_name('td')[4]
                    race_url_list.append(race_name.find_element_by_tag_name('a').get_attribute('href'))

                self.logger.info('collected race URL count : {}'.format(len(race_url_list)))
                driver.execute_script("javascript:paging('{}')".format(page_count + 2))
                time.sleep(2)

            self.logger.info('collected race URL count : {}'.format(len(race_url_list)))

        except Exception as e:
            self.logger.exception(e)

        finally:
            self.logger.info('writing result in txt file')
            with open('race_url_list.txt', 'w') as f:
                for race_url in race_url_list:
                    f.write(race_url + '\n')
            self.logger.info('finished writing')

            driver.close()


if __name__ == '__main__':
    collector = RaceURLCollector()
    collector.get_url_list()
