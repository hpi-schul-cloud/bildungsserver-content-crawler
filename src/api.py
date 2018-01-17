from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

import requests
from abc import ABC, abstractmethod
from jsonschema import ValidationError
from schul_cloud_resources_api_v1 import ApiClient, ResourceApi, auth
from schul_cloud_resources_api_v1.schema import validate_resource

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


class TargetFormat(dict):

    provider_name = "Bildungsserver Elixier"
    mime_type = "text/html"
    content_category = 'l'

    def __init__(self, attributes, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__setitem__('data', {
            "type": 'resource',
        })
        self.attributes = attributes

    @property
    def attributes(self) -> dict:
        return self['data']['attributes']

    @attributes.setter
    def attributes(self, attributes: dict):
        attributes['providerName'] = self.provider_name
        attributes['mimeType'] = self.mime_type
        attributes['contentCategory'] = self.content_category
        self["data"]["attributes"] = attributes


class TargetAPI:

    def __init__(self, base_url=settings.TARGET_URL) -> None:
        self.base_url = base_url
        client = ApiClient(base_url)
        self.set_auth()
        self.api = ResourceApi(client)
        self.threads = []

    def set_auth(self):
        if settings.API_KEY:
            auth.api_key(settings.API_KEY)
        elif settings.BASIC_AUTH_USER and settings.BASIC_AUTH_PASSWORD:
            auth.basic(settings.BASIC_AUTH_USER, settings.BASIC_AUTH_PASSWORD)
        else:
           auth.none()

    def log_request(self, response):
        print('Request finished', response)

    def add_resource(self, resource: dict):
        target_format = TargetFormat(attributes=resource)
        try:
            validate_resource(target_format.attributes)
        except ValidationError as e:
            # TODO: Logging
            print(resource)
            print(e)
            return None
        request_thread = self.api.add_resource(target_format, callback=self.log_request)
        self.threads.append(request_thread)

    def finish_all_request(self):
        for thread in self.threads:
            thread.join()
