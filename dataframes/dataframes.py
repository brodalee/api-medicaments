from pandas import DataFrame

from dataframes.compositions_dataframe import CompositionDataframe
from dataframes.generic_groups_dataframe import GenericGroupsDataframe
from dataframes.medicaments_dataframe import MedicamentDataframe
from dataframes.prescription_dataframe import PrescriptionDataframe
from dataframes.presentations_dataframe import PresentationDataframe


class Dataframes(object):
    medicaments: MedicamentDataframe
    presentations: PresentationDataframe
    composition: CompositionDataframe
    generic_groups: GenericGroupsDataframe
    prescriptions: PrescriptionDataframe

    def __init__(
            self, medicaments: DataFrame, presentations: DataFrame, compositions: DataFrame,
            generic_groups: DataFrame, prescriptions: DataFrame
    ):
        self.medicaments = MedicamentDataframe(medicaments)
        self.presentations = PresentationDataframe(presentations)
        self.composition = CompositionDataframe(compositions)
        self.generic_groups = GenericGroupsDataframe(generic_groups)
        self.prescriptions = PrescriptionDataframe(prescriptions)
