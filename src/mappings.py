class Mapping:

    def __init__(self, name: str, transform: callable = lambda m: m[0]) -> None:
        self.name = name
        self.transform_function = transform

    def transform(self, matches):
        return self.transform_function(matches)


class LanguageMapping(Mapping):
    # TODO: get mapping from settings?
    mapping = {
        "Deutsch": "de-de",
        "de": "de-de",
        "Englisch": "en-en",
        "Spanisch": "es-es",
        "Französisch": "fr-fr",
        "Polnisch": "pt",
        "Tschechisch": "cs",
        "Bulgarisch": "bg",
        "Italienisch": "it",
        "Türkisch": "tr",
        "Albanisch": "sq"
    }

    def transform(self, match):
        source_languages = match.split(';')
        try:
            return [self.mapping[language.strip()] for language in source_languages]
        except KeyError as e:
            raise ValueError('Could not map language {}'.format(e)) from e


class LicenceMapping(Mapping):
    def transform(self, match):
        return [match]
