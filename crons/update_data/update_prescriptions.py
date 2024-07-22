import pandas
import requests
import os
from dataframes.dataframes import Dataframes
from dataframes.prescription_dataframe import PrescriptionDataframe
from models.prescriptions import Prescriptions

file_path = "./.cache/CIS_CPD_bdpm.json"


def has_cache() -> bool:
    if os.path.isfile(file_path):
        return True

    return False


def get_cache(data_frame: Dataframes):
    dframe = pandas.read_json(file_path, orient="records", encoding="utf-8")
    dframe.columns = Prescriptions.columns()
    dframe.reset_index(drop=True)
    data_frame.prescriptions = PrescriptionDataframe(dframe)


def delete_cache():
    os.remove(file_path)


def make_cache(data_frame: Dataframes):
    if has_cache():
        delete_cache()

    data_frame.prescriptions.to_json(file_path)


def fetch_file():
    if has_cache():
        pass

    request = requests.get(
        "https://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_CPD_bdpm.txt"
    )

    it = request.iter_lines()
    result = []
    for line in it:
        if len(line) > 0:
            result.append(line.decode("latin-1").split("\t"))

    return result


def update_prescriptions(dataframes: Dataframes):
    print("Handling prescriptions ...")
    if has_cache():
        get_cache(dataframes)
        print("Prescriptions has cache, terminated.")
        return

    results = fetch_file()
    for line in results:
        # TODO : voir comment supprimer car identifier est partager à un group

        prescription = Prescriptions(
            cis=int(line[0]),
            condition=line[1]
        )

        dataframes.prescriptions.add_prescription(prescription)

    make_cache(dataframes)
    print("Updated prescriptions successfully !")
