import log
from lib import SponScraper, ZeitScraper, JungeFreiheitScraper
import os.path

# logger
datapath = os.path.abspath(os.path.dirname(__file__)) + '\\data\\'
logger = log.setup_custom_logger('root')
logger.info('start scraping')

#JungeFreiheitScraper.scrape(datapath)
SponScraper.scrape(datapath)
#ZeitScraper.scrape(datapath)
