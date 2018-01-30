import os

API_KEY = os.getenv('API_KEY', None)
BASIC_AUTH_USER = os.getenv('BASIC_AUTH_USER', 'schulcloud-content-1')
BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD', 'content-1')
# XML_LOCATION = os.getenv('XML_LOCATION', '../data/export.xml')  # set to 'http://www.bildungsserver.de/elixier/export.xml' for real data
XML_LOCATION = os.getenv('XML_LOCATION', '../data/siemens-stiftung.xml')  # set to 'http://www.bildungsserver.de/elixier/export.xml' for real data
SOURCE_API = os.getenv('SOURCE_API', 'LocalXmlFeed')
TARGET_URL = os.getenv('TARGET_URL', 'http://localhost:4040/resources')
