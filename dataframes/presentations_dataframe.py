import pandas
from pandas import DataFrame
from models.presentations import Presentations
from utils import french_boolean_to_real_boolean


class PresentationDataframe(object):
    _dataframe: DataFrame

    def __init__(self, presentation: DataFrame):
        self._dataframe = presentation

    def add_presentation(self, presentation: Presentations) -> None:
        self._dataframe = pandas.concat(
            [
                self._dataframe,
                pandas.DataFrame([presentation.to_dict()], columns=Presentations.columns())
            ]
        ).reset_index(drop=True)

    def drop(self, cip7: str):
        result = self._dataframe.query("cip7 == '{0}'".format(cip7))
        if len(result) == 1:
            self._dataframe = self._dataframe.drop(index=result.axes[0].values[0]).reset_index(drop=True)

    def search_one_by_cip7(self, cip7: str) -> Presentations | None:
        result = self._query("cip7 == '{0}'".format(cip7))
        if len(result) == 1:
            return result[0]

        return None

    def search_by_cis(self, cis: str) -> [Presentations]:
        return self._query("cis == {0}".format(cis))

    def _query(self, query: str) -> [Presentations]:
        rows = self._dataframe.query(query, engine="python")
        results = []
        for _, row in rows.iterrows():
            pres = Presentations(
                cis=int(row['cis']),
                cip7=int(row['cip7']),
                libelle=row['libelle'],
                statut_admin=row['statut_admin'],
                etat_commercialisation=row['etat_commercialisation'],
                date_declaration_commercialisation=row['date_declaration_commercialisation'],
                cip13=int(row['cip13']),
                agrement_collectivites=row['agrement_collectivites'],
                taux_remboursement=row['taux_remboursement'],
                prix_sans_honoraires=row['prix_sans_honoraires'],
                prix_avec_honoraires=row['prix_avec_honoraires'],
                honoraires=row['honoraires'],
                indications_remboursement=row['indications_remboursement'],
            )
            results.append(pres.to_dict())

        return results

    def to_json(self, save_to: str):
        return self._dataframe.to_json(save_to, orient="records")
