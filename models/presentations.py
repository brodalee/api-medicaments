from dataclasses import dataclass


@dataclass
class Presentations(object):
    cis: int
    cip7: int
    libelle: str
    statut_admin: str
    etat_commercialisation: str
    date_declaration_commercialisation: str
    cip13: int
    agrement_collectivites: bool
    taux_remboursement: str
    prix_sans_honoraires: str
    prix_avec_honoraires: str
    honoraires: str
    indications_remboursement: str

    def __init__(
            self, cis: int, cip7: int, libelle: str, statut_admin: str,
            etat_commercialisation: str, date_declaration_commercialisation: str,
            cip13: int, agrement_collectivites: bool, taux_remboursement: str,
            prix_sans_honoraires: str, prix_avec_honoraires: str,
            honoraires: str, indications_remboursement: str
    ):
        self.cis = cis
        self.cip7 = cip7
        self.libelle = libelle
        self.statut_admin = statut_admin
        self.etat_commercialisation = etat_commercialisation
        self.date_declaration_commercialisation = date_declaration_commercialisation
        self.cip13 = cip13
        self.agrement_collectivites = agrement_collectivites
        self.taux_remboursement = taux_remboursement
        self.prix_sans_honoraires = prix_sans_honoraires
        self.prix_avec_honoraires = prix_avec_honoraires
        self.honoraires = honoraires
        self.indications_remboursement = indications_remboursement

    @staticmethod
    def columns():
        return [
            'cis', 'cip7', 'libelle', 'statut_admin', 'etat_commercialisation',
            'date_declaration_commercialisation', 'cip13', 'agrement_collectivites',
            'taux_remboursement', 'prix_sans_honoraires', 'prix_avec_honoraires',
            'honoraires', 'indications_remboursement'
        ]

    def to_dict(self):
        result = {}
        for property, value in vars(self).items():
            result[property] = value

        return result