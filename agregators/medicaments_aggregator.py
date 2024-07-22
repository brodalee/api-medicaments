from dataframes.dataframes import Dataframes
from models.medicaments import Medicament
from utils import translate_generic_group_type
from flask import request


class MedicamentAggregator(object):
    _dataframes: Dataframes

    def __init__(self, dataframe: Dataframes):
        self._dataframes = dataframe

    def aggregate(self, medicament: Medicament):
        self._compound_presentations(medicament)
        self._compound_compositions(medicament)
        self._compound_prescriptions(medicament)
        self._compound_generic_groups(medicament)

    def _compound_presentations(self, medicament: Medicament):
        if request.args.get('withPresentations') is not None:
            medicament['presentations'] = self._dataframes.presentations.search_by_cis(medicament['cis'])

    def _compound_compositions(self, medicament: Medicament):
        if request.args.get('withCompositions') is not None:
            medicament['compositions'] = self._dataframes.composition.search_by_cis(medicament['cis'])

    def _compound_prescriptions(self, medicament: Medicament):
        if request.args.get('withPrescriptions') is not None:
            medicament['prescriptions'] = self._dataframes.prescriptions.search_by_cis(medicament['cis'])

    def _compound_generic_groups(self, medicament: Medicament):
        if request.args.get('withGenericGroups') is not None:
            medicament['generic_groups'] = self._dataframes.generic_groups.search_by_cis(medicament['cis'])
            for gg in medicament['generic_groups']:
                gg['generic_type_libelle'] = translate_generic_group_type(gg['generic_type'])