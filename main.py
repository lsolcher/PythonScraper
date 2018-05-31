import log
from lib import SponScraper

logger = log.setup_custom_logger('root')
logger.debug('main message')

SponScraper.scrape()
