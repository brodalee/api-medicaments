import pandas
from pandas import DataFrame
from models.generic_groups import GenericGroups


class GenericGroupsDataframe(object):
    _dataframe: DataFrame

    def __init__(self, dataframe: DataFrame):
        self._dataframe = dataframe

    def add_generic_group(self, generic_group: GenericGroups):
        self._dataframe = pandas.concat(
            [
                self._dataframe,
                pandas.DataFrame([generic_group.to_dict()], columns=GenericGroups.columns())
            ]
        ).reset_index(drop=True)

    def search_by_cis(self, cis: int) -> [GenericGroups]:
        return self._query("cis == {0}".format(cis))

    def drop(self, identifier: int):
        result = self._dataframe.query("identifier == {0}".format(identifier))
        if len(result) == 1:
            self._dataframe = self._dataframe.drop(index=result.axes[0].values[0]).reset_index(drop=True)

    def _query(self, query: str) -> [GenericGroups]:
        rows = self._dataframe.query(query, engine="python")
        results = []

        for _, row in rows.iterrows():
            gg = GenericGroups(
                identifier=int(row['identifier']),
                libelle=row['libelle'],
                cis=int(row['cis']),
                generic_type=int(row['generic_type']),
                order=int(row['order'])
            )
            results.append(gg.to_dict())

        return results

    def to_json(self, save_to: str):
        return self._dataframe.to_json(save_to, orient="records")
