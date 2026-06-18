# transform_station.py
# But : construire la table STATION propre (gares utilisees par les routes),
# avec matching exact + prefixe, rapport qualite et debug des non-matchees.
# Sortie : data/processed/station.csv + rapport_qualite_station.md

import json
import pandas as pd
from pathlib import Path

DOSSIER_RAW = Path("data/raw/source_station")
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
            base = nom_route.split("/")[0].strip()
            candidates = noms_stops[noms_stops.str.startswith(base, na=False)]
            if len(candidates) > 0:
                gare_choisie = candidates.iloc[0]
                gares_a_garder.add(gare_choisie)
                correspondances[nom_route] = gare_choisie

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

    # 10. Enregistrer la table.
    chemin = DOSSIER_OUT / "station.csv"
    station.to_csv(chemin, index=False, encoding="utf-8")
    print(f"\nTable STATION propre : {len(station)} lignes -> {chemin}")
    print("\nApercu :")
    print(station.head(10).to_string())

    # 11. DEBUG MATCHING : lister les gares NON associees (integre ici).
    non_associees = sorted(gares_utilisees - set(correspondances.keys()))
    print(f"\n--- DEBUG : gares non associees ({len(non_associees)}) ---")
    for nom in non_associees:
        print(f"  {nom!r}")

    # 12. Generer un rapport de qualite (traçabilite + limites connues).
    rapport = []
    rapport.append("# Rapport qualite - Table STATION")
    rapport.append("")
    rapport.append(f"- Gares brutes disponibles : {len(stops_brut)}")
    rapport.append(f"- Gares utilisees par les routes : {len(gares_utilisees)}")
    rapport.append(f"- Gares associees (exact + prefixe) : {len(correspondances)}")
    rapport.append(f"- Gares finales (apres dedoublonnage) : {len(station)}")
    rapport.append(f"- Taux de couverture : {len(correspondances) / len(gares_utilisees) * 100:.1f}%")
    rapport.append(f"- Gares sans coordonnees GPS : {int(station['latitude'].isna().sum())}")
    rapport.append("")
    rapport.append("## Limite connue : matching par prefixe")
    rapport.append("Les routes utilisent des noms de villes generiques (ex: 'Wien'),")
    rapport.append("alors que stops.json contient des gares precises (ex: 'Wien Hbf').")
    rapport.append("Le matching par prefixe peut generer des faux positifs")
    rapport.append("(ex: 'Berlin' -> 'Berlingen'). Un referentiel UIC normalise")
    rapport.append("resoudrait ce probleme. Code UIC absent des donnees sources.")
    rapport.append("")
    rapport.append(f"## Gares non associees ({len(non_associees)})")
    for nom in non_associees:
        rapport.append(f"- {nom}")

    chemin_rapport = DOSSIER_OUT / "rapport_qualite_station.md"
    chemin_rapport.write_text("\n".join(rapport), encoding="utf-8")
    print(f"\nRapport qualite -> {chemin_rapport}")

if __name__ == "__main__":
    construire_station()