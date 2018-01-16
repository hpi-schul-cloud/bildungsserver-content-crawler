from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

import requests
from abc import ABC, abstractmethod
from jsonschema import ValidationError
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

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self["data"] = {
            "type": 'resource',
        }
        if 'attributes' in kwargs:
            attributes = kwargs.pop('attributes')
            self.attributes = attributes

    @property
    def attributes(self) -> dict:
        return self['attributes']

    @attributes.setter
    def attributes(self, attributes: dict) -> dict:
        attributes['providerName'] = self.provider_name
        attributes['mimeType'] = self.mime_type
        attributes['contentCategory'] = self.content_category
        self["data"]["attributes"] = attributes
        return self["data"]["attributes"]


class TargetAPI:

    def __init__(self, base_url=settings.TARGET_URL) -> None:
        self.base_url = base_url

    # TODO: We could use schul-cloud-resources-api-v1 to handle the api requests.
    def post(self, resource: dict):
        target_format = TargetFormat(attributes=resource)
        try:
            validate_resource(target_format.attributes)
        except ValidationError as e:
            # TODO: Logging
            print(resource)
            print(e)
        else:
            request = requests.post(self.base_url, json=target_format)
            request.raise_for_status()
