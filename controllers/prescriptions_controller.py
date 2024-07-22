from flask import Response, request, jsonify
from dataframes.dataframes import Dataframes
from exceptions.bad_request import BadRequest
from models.prescriptions import Prescriptions


class PrescriptionsController(object):
    _dataframes: Dataframes

    def __init__(self, dataframes: Dataframes):
        self._dataframes = dataframes

    def get_prescriptions_by_cis(self) -> Response:
        args = request.args
        searched_cis = args.get("search")
        if searched_cis is None:
            raise BadRequest(description="Missing query string search for cis")

        result: [Prescriptions] = self._dataframes.prescriptions.search_by_cis(int(searched_cis))

        return jsonify(result)
