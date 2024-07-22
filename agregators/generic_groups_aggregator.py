from models.generic_groups import GenericGroups
from utils import translate_generic_group_type


class GenericGroupsAggregator(object):
    def aggregate(self, generic_group: GenericGroups):
        self._compound_libelle(generic_group)

    def _compound_libelle(self, generic_group: GenericGroups):
        generic_group['generic_type_libelle'] = translate_generic_group_type(generic_group['generic_type'])
