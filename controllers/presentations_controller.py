from flask import request, jsonify, Response

from dataframes.dataframes import Dataframes
from exceptions.bad_request import BadRequest
from models.presentations import Presentations


class PresentationsController(object):
    _dataframes: Dataframes

    def __init__(self, dataframes: Dataframes):
        self._dataframes = dataframes

    def get_presentations_by_cis(self) -> Response:
        args = request.args
        searched_cis = args.get("search")
        if searched_cis is None:
            raise BadRequest(description="Missing query string search for cis")

        result: [Presentations] = self._dataframes.presentations.search_by_cis(int(searched_cis))

        return jsonify(result)
