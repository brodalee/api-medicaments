import logging
from typing import Optional
import pandas
from dynaconf import FlaskDynaconf, Dynaconf
from config import settings
from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify
from flask_apscheduler.scheduler import BackgroundScheduler
from crons.update_data.main import update_data
from controllers.main import routes
from models.compositions import Compositions
from models.generic_groups import GenericGroups
from models.medicaments import Medicament
from models.prescriptions import Prescriptions
from models.presentations import Presentations
from dataframes.dataframes import Dataframes
import threading


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(process)d - [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(funcName)s() - %("
           "message)s",
)
logging.getLogger()


def init_dataframes() -> Dataframes:
    return Dataframes(
        medicaments=pandas.DataFrame(columns=Medicament.columns()),
        presentations=pandas.DataFrame(columns=Presentations.columns()),
        compositions=pandas.DataFrame(columns=Compositions.columns()),
        generic_groups=pandas.DataFrame(columns=GenericGroups.columns()),
        prescriptions=pandas.DataFrame(columns=Prescriptions.columns())
    )


def create_app(_settings: Optional[Dynaconf] = None) -> Flask:
    flask = Flask(__name__)
    # Init dynaconf
    FlaskDynaconf(flask, dynaconf_instance=_settings)

    flask.add_url_rule("/ping", "ping", lambda: ("pong", 200))

    return flask


flask_app = create_app(settings)
dataframes = init_dataframes()

scheduler = BackgroundScheduler()
# Execution toutes les 30 minutes.
scheduler.add_job(
    update_data,
    "cron",
    args=[dataframes],
    minute=30
)


def update_data_in_background():
    thread_event = threading.Event()
    thread_event.set()
    thread = threading.Thread(target=update_data, args=[dataframes])
    thread.start()


# update_data(dataframes)  # pour avoir des données dès le lancement de l'application.
scheduler.start()
update_data_in_background()


@flask_app.errorhandler(HTTPException)
def render_http_exception(error):
    logging.error("HTTPException : {error}".format(error=error))

    resp = {
        "error": {
            "status": error.name,
            "code": error.code,
            "message": error.description,
        }
    }

    return jsonify(resp), error.code


if __name__ == "__main__":
    routes(flask_app, dataframes)
    flask_app.run(debug=flask_app.config["DEBUG"])
