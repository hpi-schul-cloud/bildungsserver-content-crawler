import os

API_KEY = os.getenv('API_KEY', None)
BASIC_AUTH_USER = os.getenv('BASIC_AUTH_USER', 'schulcloud-content-1')
BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD', 'content-1')
# XML_LOCATION = os.getenv('XML_LOCATION', '../data/export.xml')
# XML_LOCATION = os.getenv('XML_LOCATION', 'http://www.bildungsserver.de/elixier/export.xml')
# XML_LOCATION = os.getenv('XML_LOCATION', '../data/siemens-stiftung.xml')
XML_LOCATION = os.getenv('XML_LOCATION', 'https://medienportal.siemens-stiftung.org/custom/api/rss2feed.php?maxage=0&lang=de')
TARGET_URL = os.getenv('TARGET_URL', 'http://localhost:4040/resources')
CRAWLER = os.getenv('CRAWLER', '')
DRY_RUN = True if os.getenv('DRY_RUN', None) is None else False
