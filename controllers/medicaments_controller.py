import math

from flask import Response, request, jsonify
from dataframes.dataframes import Dataframes
from exceptions.bad_request import BadRequest
from exceptions.not_found import NotFound
from utils import translate_generic_group_type


class MedicamentsController(object):
    _dataframes: Dataframes

    def __init__(self, dataframes: Dataframes):
        self._dataframes = dataframes

    def search_by_medicament_name(self) -> Response:
        args = request.args
        searched_name = args.get("search")
        if searched_name is None:
            raise BadRequest(description="Missing query string name")

        result = self._dataframes.medicaments.search_by_name_like(searched_name.replace("%20", " "))

        if args.get('withPresentation') is not None:
            for med in result:
                pres = self._dataframes.presentations.search_by_cis(med['cis'])
                med['presentation'] = pres

        if args.get('withCompositions') is not None:
            for med in result:
                med['compositions'] = self._dataframes.composition.search_by_cis(med['cis'])

        if args.get('withPrescriptions') is not None:
            for med in result:
                med['prescriptions'] = self._dataframes.prescriptions.search_by_cis(int(med['cis']))

        if args.get('withGenericGroups') is not None:
            for med in result:
                med['generic_groups'] = self._dataframes.generic_groups.search_by_cis(int(med['cis']))
                for gg in med['generic_groups']:
                    # Translate id to string
                    gg['generic_type'] = translate_generic_group_type(gg['generic_type'])

        return jsonify(result)

    def search_by_cis(self) -> Response:
        args = request.args
        searched_cis = args.get("search")
        if searched_cis is None:
            raise BadRequest(description="Missing query string cis")

        result = self._dataframes.medicaments.search_one_by_cis(int(searched_cis))
        if result is not None:
            if args.get('withPresentations') is not None:
                result['presentations'] = self._dataframes.presentations.search_by_cis(searched_cis)

            if args.get('withCompositions') is not None:
                result['compositions'] = self._dataframes.composition.search_by_cis(int(searched_cis))

            if args.get('withGenericGroups') is not None:
                result['generic_groups'] = self._dataframes.generic_groups.search_by_cis(int(searched_cis))
                for gg in result['generic_groups']:
                    # Translate id to string
                    gg['generic_type'] = translate_generic_group_type(gg['generic_type'])

            if args.get('withPrescriptions') is not None:
                result['prescriptions'] = self._dataframes.prescriptions.search_by_cis(int(searched_cis))

            return jsonify(result)

        raise NotFound("Medicament with cis {0} does not exist".format(searched_cis))

    def all(self) -> Response:
        # TODO : pagination
        args = request.args
        limit = args.get('limit', 50)
        page = args.get('page', 0)
        if limit > 100:
            limit = 50

        medicaments = self._dataframes.medicaments.fetch_medicaments_paginated(limit, page)
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
