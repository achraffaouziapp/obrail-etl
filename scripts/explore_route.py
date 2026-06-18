# explore_route.py
# But : voir la structure d'une route Back-on-Track (champs disponibles).

import json
from pathlib import Path

chemin = Path("data/raw/source_route/routes.json")
with open(chemin, encoding="utf-8") as f:
    routes = json.load(f)

print(f"Nombre de routes : {len(routes)}")
premiere_cle = list(routes.keys())[0]
print(f"\nExemple (cle = {premiere_cle!r}) :")
print(json.dumps(routes[premiere_cle], indent=2, ensure_ascii=False))