import pandas
import requests
import os
from dataframes.dataframes import Dataframes
from dataframes.medicaments_dataframe import MedicamentDataframe
from models.medicaments import Medicament
from utils import french_boolean_to_real_boolean

file_path = "./.cache/CIS_bdpm.json"


def has_cache() -> bool:
    if os.environ.get("FLASK_ENV") == "dev" and os.path.isfile(file_path):
        return True

    return False


def get_cache(data_frame: Dataframes):
    dframe = pandas.read_json(file_path, orient="records", encoding="utf-8")
    dframe.columns = Medicament.columns()
    dframe.reset_index(drop=True)

    data_frame.medicaments = MedicamentDataframe(dframe)


def delete_cache():
    os.remove(file_path)


def make_cache(data_frame: Dataframes):
    if has_cache():
        delete_cache()

    data_frame.medicaments.to_json(file_path)


def fetch_file():
    if has_cache():
        pass

    request = requests.get(
        "https://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_bdpm.txt"
    )

    it = request.iter_lines()
    result = []
    for line in it:
        if len(line) > 0:
            result.append(line.decode("latin-1").split("\t"))

    return result


def update_medicaments(dataframes: Dataframes):
    print("Handling medicaments ...")
    if has_cache():
        get_cache(dataframes)
        return

    results = fetch_file()
    for line in results:
        med = dataframes.medicaments.search_one_by_cis(int(line[0]))
        if med is not None:
            dataframes.medicaments.drop(int(line[0]))

        medicament = Medicament(
            cis=int(line[0]),
            denomination=line[1].strip(),
            forme_pharmaceutique=line[2].strip(),
            voies_administration=line[3].strip(),
            statut_admin_AMM=line[4].strip(),
            type_procedure_AMM=line[5].strip(),
            etat_commercialisation=line[6].strip(),
            date_AMM=line[7].strip(),
            statut_BDM=line[8].strip(),
            numero_autorisation_europeenne=line[9].strip(),
            titulaires=line[10].strip(),
            surveillance_renforcee=french_boolean_to_real_boolean(line[11].strip())
        )

        dataframes.medicaments.add_medicament(medicament)

    make_cache(dataframes)
    print("Updated medicament successfully !")
