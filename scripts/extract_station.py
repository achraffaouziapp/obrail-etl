# extract_station.py
# But : telecharger la source STATION (stops.json, Back-on-Track) dans
# data/raw/source_station, et (optionnel) explorer sa structure.

import requests
import json
from pathlib import Path

BASE_URL = "https://raw.githubusercontent.com/Back-on-Track-eu/night-train-data/main/data/latest"
FICHIER = "stops.json"
DOSSIER_SORTIE = Path("data/raw/source_station")

# Mettre a True pour afficher la structure apres telechargement.
EXPLORER = True

def extraire():
    DOSSIER_SORTIE.mkdir(parents=True, exist_ok=True)
    url = f"{BASE_URL}/{FICHIER}"
    print(f"Telechargement de {FICHIER}...")
    reponse = requests.get(url)
    if reponse.status_code == 200:
        chemin = DOSSIER_SORTIE / FICHIER
        chemin.write_text(reponse.text, encoding="utf-8")
        print(f"  OK -> {chemin}")
    else:
        print(f"  ERREUR {reponse.status_code}")

def explorer():
    chemin = DOSSIER_SORTIE / FICHIER
    with open(chemin, encoding="utf-8") as f:
        stops = json.load(f)
    print(f"\n--- EXPLORATION ---")
    print(f"Nombre de gares : {len(stops)}")
    premiere_cle = list(stops.keys())[0]
    print(f"Exemple (cle = {premiere_cle!r}) :")
    print(json.dumps(stops[premiere_cle], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    extraire()
    if EXPLORER:
        explorer()