# extract.py
# But : telecharger les fichiers Back-on-Track (routes, trips, stops...) en JSON
# depuis GitHub, vers data/raw. Source principale pour la table ROUTE.

import requests
from pathlib import Path

BASE_URL = "https://raw.githubusercontent.com/Back-on-Track-eu/night-train-data/main/data/latest"

FICHIERS = [
    "routes.json",
    "trips.json",
    "stops.json",
    "agencies.json",
]

DOSSIER_SORTIE = Path("data/raw/back_on_track")

def telecharger():
    DOSSIER_SORTIE.mkdir(parents=True, exist_ok=True)
    for nom_fichier in FICHIERS:
        url = f"{BASE_URL}/{nom_fichier}"
        print(f"Telechargement de {nom_fichier}...")
        reponse = requests.get(url)
        if reponse.status_code == 200:
            chemin = DOSSIER_SORTIE / nom_fichier
            chemin.write_text(reponse.text, encoding="utf-8")
            print(f"  OK -> {chemin}")
        else:
            print(f"  ERREUR {reponse.status_code} pour {nom_fichier}")

if __name__ == "__main__":
    telecharger()
    print("Termine.")