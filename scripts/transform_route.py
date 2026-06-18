# transform_route.py
# But : construire la table ROUTE propre a partir de routes.json (Back-on-Track).
# Sortie : data/processed/route.csv

import json
import pandas as pd
from pathlib import Path

DOSSIER_RAW = Path("data/raw/back_on_track")
DOSSIER_OUT = Path("data/processed")

def nettoyer_vide(valeur):
    """Transforme une chaine vide en None (valeur manquante propre)."""
    if valeur is None or (isinstance(valeur, str) and valeur.strip() == ""):
        return None
    return valeur

def construire_route():
    DOSSIER_OUT.mkdir(parents=True, exist_ok=True)

    # 1. Charger routes.json (un dictionnaire) en tableau pandas.
    with open(DOSSIER_RAW / "routes.json", encoding="utf-8") as f:
        routes_brut = json.load(f)
    df = pd.DataFrame(list(routes_brut.values()))
    print(f"Routes brutes : {len(df)}")

    # 2. Selectionner et renommer les colonnes utiles pour la table ROUTE.
    route = pd.DataFrame({
        "route_id": df["route_id"],
        "departure_station": df["origin_trip_0"],
        "arrival_station": df["destination_trip_0"],
        "operator": df["agency_id"],
        "distance_km": df["distance"],
        "countries": df["countries"],
    })

    # 3. Nettoyer les valeurs vides (chaines "" -> None).
    for col in ["departure_station", "arrival_station", "operator", "distance_km", "countries"]:
        route[col] = route[col].apply(nettoyer_vide)

    # 4. Convertir distance_km en nombre (ou None si pas convertible).
    route["distance_km"] = pd.to_numeric(route["distance_km"], errors="coerce")

    # 5. Supprimer les routes corrompues : sans depart OU sans arrivee.
    avant = len(route)
    route = route[route["departure_station"].notna() & route["arrival_station"].notna()]
    print(f"Routes supprimees (depart/arrivee manquant) : {avant - len(route)}")

    # 6. Supprimer les doublons sur route_id.
    avant = len(route)
    route = route.drop_duplicates(subset=["route_id"])
    print(f"Doublons supprimes : {avant - len(route)}")

    # 7. Statistiques de qualite (utile pour le dashboard).
    sans_distance = route["distance_km"].isna().sum()
    print(f"Routes sans distance : {sans_distance} / {len(route)}")

    # 8. Enregistrer.
    chemin = DOSSIER_OUT / "route.csv"
    route.to_csv(chemin, index=False, encoding="utf-8")
    print(f"\nTable ROUTE propre : {len(route)} lignes -> {chemin}")
    print("\nApercu :")
    print(route.head(10).to_string())

if __name__ == "__main__":
    construire_route()