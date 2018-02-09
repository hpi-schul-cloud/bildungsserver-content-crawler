import json
import logging
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

import jsonschema
import os
import requests
from abc import ABC, abstractmethod
from requests import HTTPError

from src.exceptions import ConfigurationError
from . import settings


class XmlFeed(ABC):
    base_url = settings.XML_LOCATION

    @abstractmethod
    def get_xml_feed(self) -> Element:
        ...


class LocalXmlFeed(XmlFeed):

    def __init__(self, file=settings.XML_LOCATION) -> None:
        self.file = file

    def get_xml_feed(self) -> Element:
        xml_tree = ET.parse(self.file)
        return xml_tree.getroot()


class BildungsserverFeed(XmlFeed):
    base_url = 'http://www.bildungsserver.de/elixier/export.xml'

    def get_xml_feed(self) -> Element:
        request = requests.get(self.base_url)
        request.raise_for_status()
        return ET.fromstring(request.text)


class LocalRssFeed(LocalXmlFeed):

    def get_xml_feed(self):
        feed = super(LocalRssFeed, self).get_xml_feed()
        return feed.find('channel').iterfind('item')


class SiemensStiftungFeed(BildungsserverFeed):
    base_url = 'https://medienportal.siemens-stiftung.org/custom/api/rss2feed.php?maxage=0&lang=de'

    def get_xml_feed(self):
        feed = super(SiemensStiftungFeed, self).get_xml_feed()
        return feed.find('channel').iterfind('item')


class ResourceAPI:
    schema = 'schema/resource-schema.json'

    def __init__(self, base_url=settings.TARGET_URL) -> None:
        self.logger = logging.getLogger('resourceAPI')
        self.base_url = base_url
        schema_path = os.path.join(os.path.dirname(__file__), self.schema)
        self.resource_schema = json.load(open(schema_path))

    def validate(self, instance):
        jsonschema.validate(instance, self.resource_schema)

    @property
    def auth(self):
        if settings.BASIC_AUTH_USER and settings.BASIC_AUTH_PASSWORD:
            return (settings.BASIC_AUTH_USER, settings.BASIC_AUTH_PASSWORD,)
        else:
            raise ConfigurationError("settings.BASIC_AUTH_USER and settings.BASIC_AUTH_PASSWORD must be set.")

    def log(self, message):
        self.logger.error(message)

    def add_resource(self, resource: dict):
        try:
            request = requests.post(self.base_url, json=resource, auth=self.auth)
            request.raise_for_status()
        except HTTPError as e:
            self.log("{} {} ".format(e, e.response.content))
        except ConnectionError as e:
            self.log(e)
            raise e
