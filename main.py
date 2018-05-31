import log
from lib import SponScraper
import os.path

# logger
i = 10
logger = log.setup_custom_logger('root')
logger.info('start scraping')
SponScraper.scrape()
