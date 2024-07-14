import os

import pandas
import requests

from dataframes.dataframes import Dataframes
from dataframes.presentations_dataframe import PresentationDataframe
from models.presentations import Presentations
from utils import french_boolean_to_real_boolean


file_path = "./.cache/CIS_CIP_bdpm.json"


def has_cache() -> bool:
    if os.environ.get("FLASK_ENV") == "dev" and os.path.isfile(file_path):
        return True

    return False


def get_cache(data_frame: Dataframes):
    dframe = pandas.read_json(file_path, orient="records", encoding="utf-8")
    dframe.columns = Presentations.columns()
    dframe.reset_index(drop=True)

    data_frame.presentations = PresentationDataframe(dframe)


def delete_cache():
    os.remove(file_path)


def make_cache(data_frame: Dataframes):
    if has_cache():
        delete_cache()

    data_frame.presentations.to_json(file_path)


def fetch_file():
    if has_cache():
        pass

    request = requests.get(
        "https://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_CIP_bdpm.txt"
    )

    it = request.iter_lines()
    result = []
    for line in it:
        if len(line) > 0:
            result.append(line.decode("latin-1").split("\t"))

    return result


def update_presentations(dataframes: Dataframes):
    print("Handling presentations ...")
    if has_cache():
        get_cache(dataframes)
        return

    results = fetch_file()
    for line in results:
        pres = dataframes.presentations.search_one_by_cip7(line[1])
        if pres is not None:
            dataframes.presentations.drop(line[1])

        presentation = Presentations(
            cis=int(line[0].strip()),
            cip7=int(line[1].strip()),
            libelle=line[2].strip(),
            statut_admin=line[3].strip(),
            etat_commercialisation=line[4].strip(),
            date_declaration_commercialisation=line[5].strip(),
            cip13=int(line[6].strip()),
            agrement_collectivites=french_boolean_to_real_boolean(line[7].strip()),
            taux_remboursement=line[8].strip(),
            prix_sans_honoraires=line[9].strip(),
            prix_avec_honoraires=line[10].strip(),
            honoraires=line[11].strip(),
            indications_remboursement=line[12].strip(),
        )

        dataframes.presentations.add_presentation(presentation)

    make_cache(dataframes)
    print("Updated presentations successfully !")
