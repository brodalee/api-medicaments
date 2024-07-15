from dataclasses import dataclass


@dataclass
class Prescriptions(object):
    cis: int
    condition: str

    def __init__(self, cis: int, condition: str):
        self.cis = cis
        self.condition = condition

    @staticmethod
    def columns():
        return [
            'cis', 'condition',
        ]

    def to_dict(self):
        result = {}
        for property, value in vars(self).items():
            result[property] = value

        return result