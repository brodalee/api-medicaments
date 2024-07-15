from dataclasses import dataclass


@dataclass
class Compositions(object):
    cis: int
    designation_pharmaceutique: str
    code: int
    denomination: str
    dosage: str
    dosage_reference: str
    nature: str
    # TODO ajouter le numéro de lien vers substances actives et fractions thérapeutiques.

    def __init__(
            self, cis: int, designation_pharmaceutique: str, code: int,
            denomination: str, dosage: str, dosage_reference: str,
            nature: str
    ):
        self.cis = cis
        self.designation_pharmaceutique = designation_pharmaceutique
        self.code = code
        self.denomination = denomination
        self.dosage = dosage
        self.dosage_reference = dosage_reference
        self.nature = nature

    @staticmethod
    def columns():
        return [
            'cis', 'designation_pharmaceutique', 'code', 'denomination',
            'dosage', 'dosage_reference', 'nature'
        ]

    def to_dict(self):
        result = {}
        for property, value in vars(self).items():
            result[property] = value

        return result
