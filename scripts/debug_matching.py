# debug_matching.py
# But : afficher les noms de gares des routes qui ne matchent PAS dans stops.json,
# pour comprendre le probleme avant de le corriger.

import json
import pandas as pd
from pathlib import Path

DOSSIER_RAW = Path("data/raw/back_on_track")
DOSSIER_OUT = Path("data/processed")

# Noms de gares dans stops.json
with open(DOSSIER_RAW / "stops.json", encoding="utf-8") as f:
    stops = json.load(f)
noms_stops = set(s["stop_name"] for s in stops.values())

# Noms de gares dans route.csv
route = pd.read_csv(DOSSIER_OUT / "route.csv")
gares_routes = set(route["departure_station"].dropna()) | set(route["arrival_station"].dropna())

# Celles qui ne matchent pas
non_matchees = sorted(gares_routes - noms_stops)
print(f"Gares non matchees : {len(non_matchees)}\n")
for nom in non_matchees:
    print(f"  {nom!r}")