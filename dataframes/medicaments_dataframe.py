import pandas
from pandas import DataFrame
from models.medicaments import Medicament


class MedicamentDataframe(object):
    _dataframe: DataFrame

    def __init__(self, dataframe: DataFrame):
        self._dataframe = dataframe

    def add_medicament(self, medicament: Medicament) -> None:
        self._dataframe = pandas.concat(
            [
                self._dataframe,
                pandas.DataFrame([medicament.to_dict()], columns=Medicament.columns())
            ]
        ).reset_index(drop=True)

    def fetch_medicaments_paginated(self, limit: int, page: int) -> [Medicament]:
        # TODO faire la pagination.
        return self._query("cis != ''")

    def total_count(self) -> int:
        return self._dataframe.size

    def search_by_name_like(self, name: str) -> [Medicament]:
        return self._query(
            "denomination.str.contains('{0}') or denomination.str.contains('{1}')".format(name, name.upper()))

    def search_one_by_cis(self, cis: int) -> Medicament | None:
        result = self._query("cis == {0}".format(cis))
        if len(result) == 1:
            return result[0]

        return None

    def _query(self, query: str) -> [Medicament]:
        rows = self._dataframe.query(query, engine="python")
        results = []
        for _, row in rows.iterrows():
            med = Medicament(
                cis=row['cis'],
                denomination=row['denomination'],
                forme_pharmaceutique=row['forme_pharmaceutique'],
                voies_administration=row['voies_administration'],
                statut_admin_AMM=row['statut_admin_AMM'],
                type_procedure_AMM=row['type_procedure_AMM'],
                etat_commercialisation=row['etat_commercialisation'],
                date_AMM=row['date_AMM'],
                statut_BDM=row['statut_BDM'],
                numero_autorisation_europeenne=row['numero_autorisation_europeenne'],
                titulaires=row['titulaires'],
                surveillance_renforcee=row['surveillance_renforcee']
            )
            results.append(med.to_dict())

        return results

    def drop(self, cis: int):
        result = self._dataframe.query("cis == {0}".format(cis))
        if len(result) == 1:
            self._dataframe = self._dataframe.drop(index=result.axes[0].values[0]).reset_index(drop=True)

    def to_json(self, save_to: str):
        return self._dataframe.to_json(save_to, orient="records")
