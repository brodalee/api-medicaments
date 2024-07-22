from flask import request, jsonify

from agregators.generic_groups_aggregator import GenericGroupsAggregator
from dataframes.dataframes import Dataframes
from exceptions.bad_request import BadRequest
from models.generic_groups import GenericGroups


class GenericGroupsController(object):
    _dataframes: Dataframes
    _aggregator: GenericGroupsAggregator

    def __init__(self, dataframes: Dataframes, aggregator: GenericGroupsAggregator):
        self._dataframes = dataframes
        self._aggregator = aggregator

    def get_generic_groups_by_cis(self):
        args = request.args
        searched_cis = args.get("search")
        if searched_cis is None:
            raise BadRequest(description="Missing query string search for cis")

        result: [GenericGroups] = self._dataframes.generic_groups.search_by_cis(int(searched_cis))
        for gg in result:
            self._aggregator.aggregate(gg)

        return jsonify(result)
