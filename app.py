from src.api import HttpXmlFeed, LocalXmlFeed, LocalRssFeed
from src.crawler import Crawler, SiemensCrawler

if __name__ == '__main__':
    crawler = SiemensCrawler(LocalRssFeed)
    crawler.crawl()
