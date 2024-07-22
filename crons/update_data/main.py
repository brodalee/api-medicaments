import threading

from crons.update_data.update_prescriptions import update_prescriptions
from crons.update_data.update_compositions import update_compositions
from crons.update_data.update_generic_groups import update_generic_groups
from crons.update_data.update_presentations import update_presentations
from crons.update_data.update_medicaments import update_medicaments
from dataframes.dataframes import Dataframes


def update_data(dataframes: Dataframes):
    update_medicaments(dataframes)
    update_presentations(dataframes)
    update_compositions(dataframes)
    update_generic_groups(dataframes)
    update_prescriptions(dataframes)
