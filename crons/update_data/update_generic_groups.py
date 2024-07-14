import pandas
import requests
import os
from dataframes.dataframes import Dataframes
from dataframes.generic_groups_dataframe import GenericGroupsDataframe
from models.generic_groups import GenericGroups

file_path = "./.cache/CIS_GENER_bdpm.json"


def has_cache() -> bool:
    if os.environ.get("FLASK_ENV") == "dev" and os.path.isfile(file_path):
        return True

    return False


def get_cache(data_frame: Dataframes):
    dframe = pandas.read_json(file_path, orient="records", encoding="utf-8")
    dframe.columns = GenericGroups.columns()
    dframe.reset_index(drop=True)

    data_frame.generic_groups = GenericGroupsDataframe(dframe)


def delete_cache():
    os.remove(file_path)


def make_cache(data_frame: Dataframes):
    if has_cache():
        delete_cache()

    data_frame.generic_groups.to_json(file_path)


def fetch_file():
    if has_cache():
        pass

    request = requests.get(
        "https://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_GENER_bdpm.txt"
    )

    it = request.iter_lines()
    result = []
    for line in it:
        if len(line) > 0:
            result.append(line.decode("latin-1").split("\t"))

    return result


def update_generic_groups(dataframes: Dataframes):
    print("Handling generic groups ...")
    if has_cache():
        get_cache(dataframes)
        return

    results = fetch_file()
    for line in results:
        # TODO : voir comment supprimer car identifier est partager à un group

        generic_group = GenericGroups(
            identifier=int(line[0].strip()),
            libelle=line[1].strip(),
            cis=int(line[2].strip()),
            generic_type=int(line[3].strip()),
            order=int(line[4].strip())
        )

        dataframes.generic_groups.add_generic_group(generic_group)

    make_cache(dataframes)
    print("Updated generic groups successfully !")
