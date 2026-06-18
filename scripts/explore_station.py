# explore_station.py
# But : voir la structure d'une gare (stops.json) et compter.

import json
from pathlib import Path

chemin = Path("data/raw/source_station/stops.json")
with open(chemin, encoding="utf-8") as f:
    stops = json.load(f)

print(f"Nombre de gares : {len(stops)}")
premiere_cle = list(stops.keys())[0]
print(f"\nExemple (cle = {premiere_cle!r}) :")
print(json.dumps(stops[premiere_cle], indent=2, ensure_ascii=False))