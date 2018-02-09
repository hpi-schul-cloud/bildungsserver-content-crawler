import argparse

from src import settings
from src.api import BildungsserverFeed, LocalXmlFeed, LocalRssFeed
from src.crawler import Crawler, SiemensCrawler, BildungsserverCrawler
from src.exceptions import ConfigurationError

if __name__ == '__main__':
    if settings.CRAWLER.lower() == 'bildungsserver':
        Crawler = BildungsserverCrawler
    elif settings.CRAWLER.lower() == 'siemens-stiftung':
        Crawler = SiemensCrawler
    else:
        raise ConfigurationError("settings.CRAWLER must be set.")

    crawler = Crawler()
    crawler.crawl()
