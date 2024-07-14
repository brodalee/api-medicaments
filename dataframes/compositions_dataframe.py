import pandas
from pandas import DataFrame
from models.compositions import Compositions


class CompositionDataframe(object):
    _dataframe: DataFrame

    def __init__(self, dataframe: DataFrame):
        self._dataframe = dataframe

    def add_composition(self, composition: Compositions) -> None:
        self._dataframe = pandas.concat(
            [
                self._dataframe,
                pandas.DataFrame([composition.to_dict()], columns=Compositions.columns())
            ]
        ).reset_index(drop=True)

    def search_by_cis(self, cis: int):
        return self._query("cis == {0}".format(cis))

    def search_one_by_code(self, code: int) -> Compositions | None:
        result = self._query("code == {0}".format(code))
        if len(result) == 1:
            return result[0]

        return None

    def drop(self, code: int):
        result = self._query("code == {0}".format(code))
        if len(result) == 1:
            self._dataframe = self._dataframe.drop(index=result.axes[0].values[0]).reset_index(drop=True)

    def to_json(self, save_to: str):
        return self._dataframe.to_json(save_to, orient="records")

    def _query(self, query: str) -> [Compositions]:
        rows = self._dataframe.query(query, engine="python")
        results = []

        for _, row in rows.iterrows():
            comp = Compositions(
                cis=int(row['cis']),
                designation_pharmaceutique=row['designation_pharmaceutique'],
                code=int(row['code']),
                denomination=row['denomination'],
                dosage=row['dosage'],
                dosage_reference=row['dosage_reference'],
                nature=row['nature']
            )
            results.append(comp.to_dict())

        return results
