import log
from lib import SponScraper
import os.path

# logger
datapath = os.path.abspath(os.path.dirname(__file__)) + '\\data\\'
logger = log.setup_custom_logger('root')
logger.info('start scraping')
SponScraper.scrape(datapath)
