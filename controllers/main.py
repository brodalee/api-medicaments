from flask import Flask

from agregators.medicaments_aggregator import MedicamentAggregator
from dataframes.dataframes import Dataframes
from controllers.medicaments_controller import MedicamentsController


def routes(app: Flask, dataframes: Dataframes):
    controller = MedicamentsController(dataframes, MedicamentAggregator(dataframes))

    app.add_url_rule("/medicaments/by-name", "/medicaments/by-name", lambda: controller.search_by_medicament_name())
    app.add_url_rule("/medicaments/by-cis", "/medicaments/by-cis", lambda: controller.search_by_cis())
    app.add_url_rule("/medicaments", "/medicaments", lambda: controller.all())
