from .api import HttpXmlFeed, LocalXmlFeed
from .crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler(LocalXmlFeed)
    crawler.crawl()