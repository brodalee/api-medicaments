class GenericGroups(object):
    identifier: int
    libelle: str
    cis: int
    generic_type: int  # TODO voir pour enum
    order: int

    def __init__(self, identifier: int, libelle: str, cis: int, generic_type: int, order: int):
        self.identifier = identifier
        self.libelle = libelle
        self.cis = cis
        self.generic_type = generic_type
        self.order = order

    @staticmethod
    def columns():
        return [
            'identifier', 'libelle', 'cis', 'generic_type', 'order'
        ]

    def to_dict(self):
        result = {}
        for property, value in vars(self).items():
            result[property] = value

        return result
