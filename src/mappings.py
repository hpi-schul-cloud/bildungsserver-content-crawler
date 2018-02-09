class Mapping:

    def __init__(self, name: str, transform: callable = lambda m: m[0]) -> None:
        self.name = name
        self.transform_function = transform

    def transform(self, matches):
        return self.transform_function(matches)

