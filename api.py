from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

import requests
from abc import ABC, abstractmethod
from schul_cloud_resources_api_v1.schema import validate_resource

import settings


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

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self["data"] = {
            "type": 'resource',
        }
        if 'attributes' in kwargs:
            attributes = kwargs.pop('attributes')
            self.attributes = attributes

    @property
    def attributes(self):
        return self['attributes']

    @attributes.setter
    def attributes(self, attributes: dict):
        attributes['providerName'] = self.provider_name
        attributes['mimeType'] = self.mime_type
        attributes['contentCategory'] = self.content_category
        self["data"]["attributes"] = attributes
        return self


class TargetAPI:

    def __init__(self, base_url=settings.TARGET_URL) -> None:
        self.base_url = base_url

    def post(self, resource: dict):
        target_format = TargetFormat(attributes=resource)
        validate_resource(target_format.attributes)
        request = requests.post(self.base_url, json=target_format)
        request.raise_for_status()