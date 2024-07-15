import json.encoder
import math
from flask import Response, request, jsonify
from agregators.medicaments_aggregator import MedicamentAggregator
from dataframes.dataframes import Dataframes
from exceptions.bad_request import BadRequest
from exceptions.not_found import NotFound
from utils import translate_generic_group_type


class MedicamentsController(object):
    _dataframes: Dataframes
    aggregator: MedicamentAggregator

    def __init__(self, dataframes: Dataframes, medicament_aggregator: MedicamentAggregator):
        self._dataframes = dataframes
        self.aggregator = medicament_aggregator

    def search_by_medicament_name(self) -> Response:
        args = request.args
        searched_name = args.get("search")
        if searched_name is None:
            raise BadRequest(description="Missing query string name")

        result = self._dataframes.medicaments.search_by_name_like(searched_name.replace("%20", " "))

        for med in result:
            self.aggregator.aggregate(med)

        return jsonify(result)

    def search_by_cis(self) -> Response:
        args = request.args
        searched_cis = args.get("search")
        if searched_cis is None:
            raise BadRequest(description="Missing query string cis")

        result = self._dataframes.medicaments.search_one_by_cis(int(searched_cis))
        if result is not None:
            self.aggregator.aggregate(result)
            return jsonify(result)

        raise NotFound("Medicament with cis {0} does not exist".format(searched_cis))

    def all(self) -> Response:
        args = request.args
        limit = int(args.get('limit', 50))
        page = int(args.get('page', 1))
        if limit > 100:
            limit = 50

        medicaments = self._dataframes.medicaments.fetch_medicaments_paginated(limit, page)
        for med in medicaments:
            self.aggregator.aggregate(med)

        total_count = self._dataframes.medicaments.total_count()
        total_page = math.ceil(total_count / limit)

        previous = page - 1 if page > 0 else None
        next = page + 1 if page < total_page else None

        response = {
            "totalPage": total_page,
            "totalCount": total_count,
            "previous": previous,
            "next": next,
            "items": medicaments
        }

        return jsonify(response)
