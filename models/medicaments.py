from models.compositions import Compositions
from models.generic_groups import GenericGroups
from models.prescriptions import Prescriptions
from models.presentations import Presentations


class Medicament(object):
    cis: int
    denomination: str
    forme_pharmaceutique: str
    voies_administration: str
    statut_admin_AMM: str
    type_procedure_AMM: str
    etat_commercialisation: str
    date_AMM: str
    statut_BDM: str
    numero_autorisation_europeenne: str
    titulaires: str
    surveillance_renforcee: bool

    # Aggregated properties
    presentations: [Presentations] = None
    compositions: [Compositions] = None
    prescriptions: [Prescriptions] = None
    generic_groups: [GenericGroups] = None

    def __init__(
            self, cis: int, denomination: str, forme_pharmaceutique: str, voies_administration: str,
            statut_admin_AMM: str, type_procedure_AMM: str, etat_commercialisation: str,
            date_AMM: str, statut_BDM: str, numero_autorisation_europeenne: str,
            titulaires: str, surveillance_renforcee: bool
    ):
        self.cis = cis
        self.denomination = denomination
        self.forme_pharmaceutique = forme_pharmaceutique
        self.voies_administration = voies_administration
        self.statut_admin_AMM = statut_admin_AMM
        self.type_procedure_AMM = type_procedure_AMM
        self.etat_commercialisation = etat_commercialisation
        self.date_AMM = date_AMM
        self.statut_BDM = statut_BDM
        self.numero_autorisation_europeenne = numero_autorisation_europeenne
        self.titulaires = titulaires
        self.surveillance_renforcee = surveillance_renforcee

    @staticmethod
    def columns():
        return [
            'cis', 'denomination', 'forme_pharmaceutique',
            'voies_administration', 'statut_admin_AMM',
            'type_procedure_AMM', 'etat_commercialisation',
            'date_AMM', 'statut_BDM', 'numero_autorisation_europeenne',
            'titulaires', 'surveillance_renforcee'
        ]

    def to_dict(self):
        result = {}
        for property, value in vars(self).items():
            result[property] = value

        return result
