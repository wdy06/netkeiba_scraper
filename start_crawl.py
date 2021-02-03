from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from netkeiba_scraper_python.spiders import raceresult

configure_logging({'LOG_ENABLEED': True,
                   'LOG_FILE': 'test.txt',
                   'LOG_LEVEL': 'INFO',
                   })
#process = CrawlerProcess(get_project_settings())
process = CrawlerProcess()

# 'followall' is the name of one of the spiders of the project.
process.crawl(raceresult.RaceResultSpider)
process.start()  # the script will block here until the crawling is finished
