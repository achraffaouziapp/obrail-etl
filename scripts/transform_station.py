# build_station.py
# But : construire la table STATION propre, limitee aux gares reellement
# utilisees par les routes (departure_station / arrival_station de route.csv).
# Sortie : data/processed/station.csv

import json
import pandas as pd
from pathlib import Path

DOSSIER_RAW = Path("data/raw/back_on_track")
DOSSIER_OUT = Path("data/processed")

def nettoyer_vide(valeur):
    if valeur is None or (isinstance(valeur, str) and valeur.strip() == ""):
        return None
    return valeur

def construire_station():
    DOSSIER_OUT.mkdir(parents=True, exist_ok=True)

    # 1. Charger toutes les gares brutes.
    with open(DOSSIER_RAW / "stops.json", encoding="utf-8") as f:
        stops_brut = json.load(f)
    stops = pd.DataFrame(list(stops_brut.values()))
    print(f"Gares brutes (toutes) : {len(stops)}")

    # 2. Charger ROUTE pour savoir quelles gares sont utilisees.
    route = pd.read_csv(DOSSIER_OUT / "route.csv")
    gares_utilisees = set(route["departure_station"].dropna()) | set(route["arrival_station"].dropna())
    print(f"Gares utilisees par les routes : {len(gares_utilisees)}")
    
    
    # 3. Garder les gares utilisees : d'abord match exact, puis match par prefixe.
    noms_stops = stops["stop_name"].dropna()

    gares_a_garder = set()
    correspondances = {}  # nom_ville_route -> nom_gare_reelle

    for nom_route in gares_utilisees:
        # a) Match exact
        if nom_route in set(noms_stops):
            gares_a_garder.add(nom_route)
            correspondances[nom_route] = nom_route
        else:
            # b) Match par prefixe : "Wien" -> premiere gare "Wien ..."
            #    On nettoie le nom (enleve la partie apres "/" pour les bilingues).
            base = nom_route.split("/")[0].strip()
            candidates = noms_stops[noms_stops.str.startswith(base, na=False)]
            if len(candidates) > 0:
                gare_choisie = candidates.iloc[0]
                gares_a_garder.add(gare_choisie)
                correspondances[nom_route] = gare_choisie

    print(f"Gares utilisees par les routes : {len(gares_utilisees)}")
    print(f"Gares effectivement associees : {len(correspondances)}")

    stops = stops[stops["stop_name"].isin(gares_a_garder)]
    print(f"Gares retenues (apres filtre) : {len(stops)}")

   

    # 4. Selectionner et renommer les colonnes pour la table STATION.
    station = pd.DataFrame({
        "station_name": stops["stop_name"],
        "station_code": stops["stop_uic_code"],
        "latitude": stops["stop_lat"],
        "longitude": stops["stop_lon"],
        "country": stops["stop_country"],
    })

    # 5. Nettoyer les vides.
    for col in ["station_code", "country"]:
        station[col] = station[col].apply(nettoyer_vide)

    # 6. Convertir lat/lon en nombres.
    station["latitude"] = pd.to_numeric(station["latitude"], errors="coerce")
    station["longitude"] = pd.to_numeric(station["longitude"], errors="coerce")

    # 7. Supprimer doublons sur le nom de gare.
    avant = len(station)
    station = station.drop_duplicates(subset=["station_name"])
    print(f"Doublons supprimes : {avant - len(station)}")

    # 8. Creer un identifiant numerique (station_id) propre.
    station = station.reset_index(drop=True)
    station.insert(0, "station_id", range(1, len(station) + 1))

    # 9. Statistiques de qualite.
    sans_gps = station["latitude"].isna().sum()
    print(f"Gares sans coordonnees GPS : {sans_gps} / {len(station)}")

    # 10. Enregistrer.
    chemin = DOSSIER_OUT / "station.csv"
    station.to_csv(chemin, index=False, encoding="utf-8")
    print(f"\nTable STATION propre : {len(station)} lignes -> {chemin}")
    print("\nApercu :")
    print(station.head(10).to_string())

if __name__ == "__main__":
    construire_station()