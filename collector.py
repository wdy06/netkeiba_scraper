# -*- coding: utf-8 -*-

import logging
import time
from multiprocessing import Process
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


class URLCollector:
    def __init__(self, logger=None):
        if logger is None:
            self.logger = logging.getLogger(__name__)
            self.formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(name)s %(filename)s'
                                               ':%(lineno)d %(message)s')

            self.handler = logging.StreamHandler()
            self.handler.setFormatter(self.formatter)
            self.handler.setLevel(logging.DEBUG)
            self.logger.setLevel(logging.DEBUG)
            self.logger.addHandler(self.handler)
        else:
            self.logger = logger

        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        # for linux
        # self.chrome_options.binary_location = '/usr/bin/google-chrome-stable'

        self.chrome_driver_path = './python/chromedriver'
        self.output_dir = './netkeiba_scraper_python/spider/data/'


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
            with open(os.path.join(self.output_dir, 'race_url_list.txt', 'w')) as f:
                for race_url in race_url_list:
                    f.write(race_url + '\n')
            self.logger.info('finished writing')

            driver.close()


class HorseURLCollector(URLCollector):
    def get_url_list(self):

        try:
            self.logger.info("start")

            driver = webdriver.Chrome(self.chrome_driver_path, chrome_options=self.chrome_options)
            target_url = 'http://db.netkeiba.com/?pid=horse_search_detail'
            driver.get(target_url)
            self.logger.info('connection success')

            element = driver.find_element_by_css_selector('#db_search_detail_form > form > table > tbody '
                                                          '> tr:nth-child(16) > td > select')
            Select(element).select_by_value('100')
            driver.find_element_by_xpath('//*[@id="db_search_detail_form"]/form/div/input[1]').submit()
            time.sleep(2)

            assert driver.find_element_by_tag_name('h2').text == u'年齢[2歳～無指定]の検索結果', \
                'This is not expected page.'

            # get total race count
            pager = driver.find_element_by_id('contents_liquid').find_element_by_class_name('pager')
            pages = pager.text.replace(',', '')
            total_horse_count = int(pages[:pages.find(u'件')])
            self.logger.info('total horse count {}'.format(total_horse_count))

            horse_url_list = []
            for page_count in range(total_horse_count // 100 + 1):
                pager = driver.find_element_by_id('contents_liquid').find_element_by_class_name('pager')
                pages = pager.text.replace(',', '')
                self.logger.info(pages[:pages.find(u'目')])

                race_table = driver.find_element_by_class_name('race_table_01')
                for i, race_element in enumerate(race_table.find_elements_by_tag_name('tr')):
                    if i == 0:
                        continue
                    horse_name = race_element.find_elements_by_tag_name('td')[1]
                    horse_url_list.append(horse_name.find_element_by_tag_name('a').get_attribute('href'))

                self.logger.info('collected horse URL count : {}'.format(len(horse_url_list)))
                driver.execute_script("javascript:paging('{}')".format(page_count + 2))
                time.sleep(2)

            self.logger.info('collected horse URL count : {}'.format(len(horse_url_list)))

        except Exception as e:
            self.logger.exception(e)

        finally:
            self.logger.info('writing result in txt file')
            with open(os.path.join(self.output_dir, 'horse_url_list.txt', 'w')) as f:
                for horse_url in horse_url_list:
                    f.write(horse_url + '\n')
            self.logger.info('finished writing')

            driver.close()


class JockeyURLCollector(URLCollector):
    def get_url_list(self):

        try:
            self.logger.info("start")

            driver = webdriver.Chrome(self.chrome_driver_path, chrome_options=self.chrome_options)
            target_url = 'http://db.netkeiba.com/?pid=jockey_search_detail'
            driver.get(target_url)
            self.logger.info('connection success')

            driver.find_element_by_id("check_act_0").click()
            driver.find_element_by_id("check_act_1").click()
            element = driver.find_element_by_css_selector('#db_search_detail_form > form > table > tbody '
                                                          '> tr:nth-child(4) > td > select')
            Select(element).select_by_value('100')
            driver.find_element_by_xpath('//*[@id="db_search_detail_form"]/form/div/input[1]').submit()
            time.sleep(2)

            assert driver.find_element_by_tag_name('h2').text == u'現役、引退の検索結果', \
                'This is not expected page.'

            # get total race count
            pager = driver.find_element_by_id('contents_liquid').find_element_by_class_name('pager')
            pages = pager.text.replace(',', '')
            total_jockey_count = int(pages[:pages.find(u'件')])
            self.logger.info('total jockey count {}'.format(total_jockey_count))

            jockey_url_list = []
            for page_count in range(total_jockey_count // 100 + 1):

                pager = driver.find_element_by_id('contents_liquid').find_element_by_class_name('pager')
                pages = pager.text.replace(',', '')
                self.logger.info(pages[:pages.find(u'目')])

                race_table = driver.find_element_by_class_name('race_table_01')
                for i, race_element in enumerate(race_table.find_elements_by_tag_name('tr')):
                    if i < 2:
                        continue
                    jockey_name = race_element.find_elements_by_tag_name('td')[0]
                    org_url = jockey_name.find_element_by_tag_name('a').get_attribute('href')
                    profile_url = org_url.replace('jockey', 'jockey/profile')
                    jockey_url_list.append(profile_url)

                self.logger.info('collected race URL count : {}'.format(len(jockey_url_list)))
                driver.execute_script("javascript:paging('{}')".format(page_count + 2))
                time.sleep(2)

            self.logger.info('collected race URL count : {}'.format(len(jockey_url_list)))

        except Exception as e:
            self.logger.exception(e)

        finally:
            self.logger.info('writing result in txt file')
            with open(os.path.join(self.output_dir, 'jockey_url_list.txt', 'w')) as f:
                for jockey_url in jockey_url_list:
                    f.write(jockey_url + '\n')
            self.logger.info('finished writing')

            driver.close()


if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(name)s %(processName)s '
                                  '%(filename)s:%(lineno)d %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    race_collector = Process(name='race_collector', target=RaceURLCollector(logger=logger).get_url_list)
    horse_collector = Process(name='horse_collector', target=HorseURLCollector(logger=logger).get_url_list)
    jockey_collector = Process(name='jockey_collector', target=JockeyURLCollector(logger=logger).get_url_list)

    race_collector.start()
    horse_collector.start()
    jockey_collector.start()
