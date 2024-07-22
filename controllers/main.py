from flask import Flask

from agregators.generic_groups_aggregator import GenericGroupsAggregator
from agregators.medicaments_aggregator import MedicamentAggregator
from controllers.compositions_controller import CompositionsController
from controllers.generic_groups_controller import GenericGroupsController
from controllers.prescriptions_controller import PrescriptionsController
from controllers.presentations_controller import PresentationsController
from dataframes.dataframes import Dataframes
from controllers.medicaments_controller import MedicamentsController


def routes(app: Flask, dataframes: Dataframes):
    medicaments_controller = MedicamentsController(dataframes, MedicamentAggregator(dataframes))
    prescriptions_controller = PrescriptionsController(dataframes)
    presentations_controller = PresentationsController(dataframes)
    compositions_controller = CompositionsController(dataframes)
    generic_groups_controller = GenericGroupsController(dataframes, GenericGroupsAggregator())

    app.add_url_rule("/medicaments/by-name", "/medicaments/by-name", lambda: medicaments_controller.search_by_medicament_name())
    app.add_url_rule("/medicaments/by-cis", "/medicaments/by-cis", lambda: medicaments_controller.search_by_cis())
    app.add_url_rule("/medicaments", "/medicaments", lambda: medicaments_controller.all())

    app.add_url_rule("/prescriptions/by-cis", "prescriptions/by-cis", lambda: prescriptions_controller.get_prescriptions_by_cis())

    app.add_url_rule("/presentations/by-cis", "presentations/by-cis", lambda: presentations_controller.get_presentations_by_cis())

    app.add_url_rule("/compositions/by-cis", "compositions/by-cis", lambda: compositions_controller.get_compositions_by_cis())

    app.add_url_rule("/generic-groups/by-cis", "generic-groups/by-cis", lambda: generic_groups_controller.get_generic_groups_by_cis())
