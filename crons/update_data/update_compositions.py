import pandas
import requests
import os
from dataframes.compositions_dataframe import CompositionDataframe
from dataframes.dataframes import Dataframes
from models.compositions import Compositions

file_path = "./.cache/CIS_COMPO_bdpm.json"


def has_cache() -> bool:
    if os.path.isfile(file_path):
        return True

    return False


def get_cache(data_frame: Dataframes):
    dframe = pandas.read_json(file_path, orient="records", encoding="utf-8")
    dframe.columns = Compositions.columns()
    dframe.reset_index(drop=True)
    data_frame.composition = CompositionDataframe(dframe)


def delete_cache():
    os.remove(file_path)


def make_cache(data_frame: Dataframes):
    if has_cache():
        delete_cache()

    data_frame.composition.to_json(file_path)


def fetch_file():
    if has_cache():
        pass

    request = requests.get(
        "https://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_COMPO_bdpm.txt"
    )

    it = request.iter_lines()
    result = []
    for line in it:
        if len(line) > 0:
            result.append(line.decode("latin-1").split("\t"))

    return result


def update_compositions(dataframes: Dataframes):
    print("Handling compositions ...")
    if has_cache():
        get_cache(dataframes)
        print("Compositions has cache, terminated.")
        return

    results = fetch_file()
    for line in results:
        comp = dataframes.composition.search_one_by_code(int(line[0]))
        if comp is not None:
            dataframes.composition.drop(int(line[0]))

        composition = Compositions(
            cis=int(line[0]),
            designation_pharmaceutique=line[1],
            code=int(line[2]),
            denomination=line[3],
            dosage=line[4],
            dosage_reference=line[5],
            nature=line[6]
        )

        dataframes.composition.add_composition(composition)

    make_cache(dataframes)
    print("Updated compositions successfully !")
