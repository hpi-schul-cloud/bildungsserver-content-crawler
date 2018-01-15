class Mapping:

    def __init__(self, name: str, transform: callable = lambda m: m) -> None:
        self.name = name
        self.transform_function = transform

    def transform(self, match):
        return self.transform_function(match)


class LanguageMapping(Mapping):
    mapping = {
        "Deutsch": "de-de",
        "de": "de-de",
        "Englisch": "en-en",
    }

    def transform(self, match):
        source_languages = match.split(';')
        try:
            return [self.mapping[language] for language in source_languages]
        except KeyError as e:
            raise ValueError('Could not map language {}'.format(e)) from e


class LicenceMapping(Mapping):
    def transform(self, match):
        return [{
            "value": match,
            'copyrighted': True
        }]