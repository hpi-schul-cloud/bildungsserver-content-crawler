from xml.etree.ElementTree import Element

from .api import LocalXmlFeed, TargetAPI, HttpXmlFeed
from .mappings import Mapping, LanguageMapping, LicenceMapping


class Crawler:
    target_to_source_mapping = {
        "title": Mapping("titel"),
        "url": Mapping("url_ressource"),
        "description": Mapping("beschreibung"),
        "licenses": LicenceMapping("rechte"),
        "mimeType": None,
        "contentCategory": None,
        "languages": LanguageMapping("sprache"),
        "tags": Mapping("schlagwort", lambda m: m.split(';')),
        "thumbnail": None,
        "dimensions": None,
        "duration": None,
        "providerName": None,
    }

    def __init__(self, source_api=LocalXmlFeed, target_api=TargetAPI) -> None:
        self.source_api = source_api()
        self.target_api = target_api()

    def crawl(self):
        feed = self.source_api.get_xml_feed()
        for child in feed:
            resource_dict = self.parse(child)
            self.target_api.post(resource_dict)

    def parse(self, element: Element) -> dict:
        target_dict = {key: '' for key in self.target_to_source_mapping if
                       self.target_to_source_mapping[key] is not None}
        for key in target_dict.keys():
            transformation = self.target_to_source_mapping[key]
            matches = element.findall(transformation.name)
            # TODO: Some items don't have all required fields set. Options:
            # - Set dummy here match if field is required.
            # - Catch validation error and log the failing resource
            # - Set default values in TargetFormat
            for match in matches:
                # TODO: if multiple entries with the same tag exist, only the last is saved and posted to the target api
                target_dict[key] = transformation.transform(match.text)
        return target_dict

