from xml.etree.ElementTree import Element

from .api import LocalXmlFeed, ResourceAPI, HttpXmlFeed
from .mappings import Mapping, LanguageMapping, LicenceMapping


class Crawler:
    target_to_source_mapping = {
        "title": Mapping("titel"),
        "url": Mapping("url_ressource"),
        "originId": Mapping('id_local'),
        "description": Mapping("beschreibung"),
        "licenses": Mapping("rechte", lambda m: m),
        "mimeType": None,
        "contentCategory": None,
        # "languages": LanguageMapping("sprache"),
        "tags": Mapping("schlagwort", lambda m: [w.strip() for w in m[0].split(';')]),
        "thumbnail": None,
        "providerName": None,
    }

    def __init__(self, source_api=LocalXmlFeed, target_api=ResourceAPI) -> None:
        self.source_api = source_api()
        self.target_api = target_api()

    def crawl(self):
        feed = self.source_api.get_xml_feed()
        for child in feed:
            resource_dict = self.parse(child)
            self.target_api.add_resource(resource_dict)

    def parse(self, element: Element) -> dict:
        target_dict = {key: '' for key in self.target_to_source_mapping if
                       self.target_to_source_mapping[key] is not None}
        for key in target_dict.keys():
            transformation = self.target_to_source_mapping[key]
            matches = element.findall(transformation.name)
            # TODO: Some items don't have all required fields set. Currently, the error is printed to stdout. Options:
            # - Set dummy here match if field is required.
            # - Catch validation error and log the failing resource
            # - Set default values in TargetFormat
            if matches:
                target_dict[key] = transformation.transform([match.text for match in matches])
        return target_dict


class SiemensCrawler(Crawler):
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
