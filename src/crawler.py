import logging
from xml.etree.ElementTree import Element

from jsonschema import ValidationError

from .api import LocalXmlFeed, ResourceAPI, BildungsserverFeed, SiemensStiftungFeed
from .mappings import Mapping


class ResourceSchema(dict):
    mime_type = 'text/html'
    content_category = 'learning-object'

    def __init__(self, provider_name, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__setitem__('mimeType', self.mime_type)
        self.__setitem__('contentCategory', self.content_category)
        self.__setitem__('providerName', provider_name)
        # TODO: Empty licence is accepted by the resource api
        if kwargs.get('licenses', None) is None:
            self.__setitem__('licenses', [''])


class Crawler:

    provider_name = None
    target_to_source_mapping = None
    source_api = None

    def __init__(self, target_api=ResourceAPI) -> None:
        self.logger = logging.getLogger(self.provider_name)
        self.source_api = self.source_api()
        self.target_api = target_api()

    def log(self, message):
        self.logger.error(message)

    def crawl(self):
        feed = self.source_api.get_xml_feed()
        for child in feed:
            resource_dict = self.parse(child)
            resource = self.validate(resource_dict)
            if resource:
                self.target_api.add_resource(resource)

    def parse(self, element: Element) -> dict:
        target_dict = {key: '' for key in self.target_to_source_mapping if
                       self.target_to_source_mapping[key] is not None}
        for key in target_dict.keys():
            transformation = self.target_to_source_mapping[key]
            matches = element.findall(transformation.name)
            if matches:
                target_dict[key] = transformation.transform([match.text for match in matches])
        return target_dict

    def validate(self, resource_dict):
        target_format = ResourceSchema(self.provider_name, **resource_dict)
        try:
            self.target_api.validate(target_format)
        except ValidationError as e:
            # self.log(e)
            return None
        return target_format


class BildungsserverCrawler(Crawler):
    provider_name = "Bildungsserver"
    source_api = BildungsserverFeed

    target_to_source_mapping = {
        "title": Mapping("titel"),
        "url": Mapping("url_ressource"),
        "originId": Mapping('id_local'),
        "description": Mapping("beschreibung"),
        "licenses": Mapping("rechte", lambda m: m),
        "mimeType": None,
        "contentCategory": None,
        "tags": Mapping("schlagwort", lambda m: [w.strip() for w in m[0].split(';')]),
        "thumbnail": None,
        "providerName": None,
    }


class SiemensCrawler(Crawler):
    provider_name = "Siemens-Stiftung"
    source_api = SiemensStiftungFeed

    target_to_source_mapping = {
        "title": Mapping("title"),
        "url": Mapping("link"),
        "originId": Mapping('guid'),
        "description": Mapping("description"),
        "licenses": None,
        "mimeType": None,
        "contentCategory": None,
        "tags": Mapping("category"),
        "thumbnail": None,
        "providerName": None,
    }
