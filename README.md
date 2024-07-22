# API Rest pour la Base de Données Publique des Médicaments (PYTHON)

## Requirements
- Python > 3.11

## Installation

Dans un terminal, à la racine du projet, lancer la commande `pip install` afin d'installer les dépendances du projet.

Dans le dossier `config`, veuillez copier le `.env.dist` en `.env` et inscrire les valeurs souhaitées.

## Run

Pour lancer le projet, mettez vous dans un terminal, et lancer la commande `python main.py`.

Vous pouvez acceder à l'API via http://localhost:5000
Pour plus d'information sur comment utiliser l'API, rendez-vous sur le swagger : http://localhost:5000/swagger

## Fonctionnement

Au démarage du projet, celui-ci va télécharger les fichiers nécéssaires afin de remplir Pandas, qui va nous servir de "BDD" ici.

Cela va générer du cache afin de rendre le prochain lancement plus rapide.

Une tâche cron sera éxécutée toutes les 30 minutes afin de maintenir à jour les données.