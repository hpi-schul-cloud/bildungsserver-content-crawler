import json
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

import jsonschema
import os
import requests
from abc import ABC, abstractmethod
from jsonschema import ValidationError
from requests import HTTPError

from . import settings


class XmlFeed(ABC):
    @abstractmethod
    def get_xml_feed(self) -> Element:
        ...


class HttpXmlFeed(XmlFeed):

    def __init__(self, base_url=settings.XML_LOCATION) -> None:
        self.base_url = base_url

    def get_xml_feed(self) -> Element:
        request = requests.get(self.base_url)
        request.raise_for_status()
        return ET.fromstring(request.text)


class LocalXmlFeed(XmlFeed):

    def __init__(self, file=settings.XML_LOCATION) -> None:
        self.file = file

    def get_xml_feed(self) -> Element:
        xml_tree = ET.parse(self.file)
        return xml_tree.getroot()


class ResourceSchema(dict):

    provider_name = "Bildungsserver Elixier"
    mime_type = 'text/html'
    content_category = 'learning-object'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__setitem__('mimeType', self.mime_type)
        self.__setitem__('contentCategory', self.content_category)
        self.__setitem__('providerName', self.provider_name)


class ResourceAPI:

    schema = 'schema/resource-schema.json'

    def __init__(self, base_url=settings.TARGET_URL) -> None:
        self.base_url = base_url
        self.threads = []
        schema_path = os.path.join(os.path.dirname(__file__), self.schema)
        self.resource_schema = json.load(open(schema_path))

    def validate(self, instance):
        jsonschema.validate(instance, self.resource_schema)

    @property
    def auth(self):
        if settings.BASIC_AUTH_USER and settings.BASIC_AUTH_PASSWORD:
            return (settings.BASIC_AUTH_USER, settings.BASIC_AUTH_PASSWORD, )

    def log_request(self, response):
        print('Request finished', response)

    def log(self, error):
        # TODO: Logging
        print(error)

    def add_resource(self, resource: dict):
        target_format = ResourceSchema(**resource)
        try:
            self.validate(target_format)
        except ValidationError as e:
            self.log(e)
            return None

        try:
            # TODO: use auth from settings
            request = requests.post(self.base_url, json=target_format, auth=self.auth)
            request.raise_for_status()
        except HTTPError as e:
            self.log(e)
