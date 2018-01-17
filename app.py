from src.api import HttpXmlFeed, LocalXmlFeed
from src.crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler(LocalXmlFeed)
    crawler.crawl()
