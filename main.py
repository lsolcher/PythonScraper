import log
from lib import SponScraper, SzScraper, JungeFreiheitScraper
import os.path

# logger
datapath = os.path.abspath(os.path.dirname(__file__)) + '\\data\\'
logger = log.setup_custom_logger('root')
logger.info('start scraping')


SzScraper.scrape(datapath)
#JungeFreiheitScraper.scrape(datapath)
#SponScraper.scrape(datapath)
#ZeitScraper.scrape(datapath)
