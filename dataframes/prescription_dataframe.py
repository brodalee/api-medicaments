import pandas
from pandas import DataFrame
from models.prescriptions import Prescriptions


class PrescriptionDataframe(object):
    _dataframe: DataFrame

    def __init__(self, dataframe: DataFrame):
        self._dataframe = dataframe

    def add_prescription(self, prescription: Prescriptions):
        self._dataframe = pandas.concat(
            [
                self._dataframe,
                pandas.DataFrame([prescription.to_dict()], columns=Prescriptions.columns())
            ]
        ).reset_index(drop=True)

    def search_by_cis(self, cis: int):
        print("SIZE :: ", self._dataframe.size)
        return self._query("cis == {0}".format(cis))

    def _query(self, query: str) -> [Prescriptions]:
        rows = self._dataframe.query(query, engine="python")
        results = []
        for _, row in rows.iterrows():
            pres = Prescriptions(
                cis=row['cis'],
                condition=row['condition']
            )
            results.append(pres.to_dict())

        return results

    def to_json(self, save_to: str):
        return self._dataframe.to_json(save_to, orient="records")
