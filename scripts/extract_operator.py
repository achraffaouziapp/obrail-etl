import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import date

# 🌐 Source web pour récupérer des opérateurs ferroviaires européens
url = "https://en.wikipedia.org/wiki/List_of_European_railways"

# 📌 Codes pays utiles pour notre MPD
country_codes = {
    "Albania": "AL",
    "Armenia": "AM",
    "Austria": "AT",
    "Azerbaijan": "AZ",
    "Belarus": "BY",
    "Belgium": "BE",
    "Bosnia and Herzegovina": "BA",
    "Bulgaria": "BG",
    "Croatia": "HR",
    "Cyprus": "CY",
    "Czechia": "CZ",
    "Czech Republic": "CZ",
    "Denmark": "DK",
    "Estonia": "EE",
    "Finland": "FI",
    "France": "FR",
    "Georgia": "GE",
    "Germany": "DE",
    "Greece": "GR",
    "Hungary": "HU",
    "Ireland": "IE",
    "Italy": "IT",
    "Kazakhstan": "KZ",
    "Latvia": "LV",
    "Liechtenstein": "LI",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Moldova": "MD",
    "Monaco": "MC",
    "Montenegro": "ME",
    "Netherlands": "NL",
    "North Macedonia": "MK",
    "Norway": "NO",
    "Poland": "PL",
    "Portugal": "PT",
    "Romania": "RO",
    "Russia": "RU",
    "San Marino": "SM",
    "Serbia": "RS",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Spain": "ES",
    "Switzerland": "CH",
    "Sweden": "SE",
    "Turkey": "TR",
    "Ukraine": "UA",
    "United Kingdom": "GB",
    "Vatican City": "VA"
}


def clean_text(text):
    # Supprimer les références du type [1], [2]
    text = re.sub(r"\[\d+\]", "", text)

    # Remplacer plusieurs espaces par un seul espace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_operator_code(text):
    # Récupérer les textes entre parenthèses : SNCF, DB, ÖBB...
    matches = re.findall(r"\(([^()]*)\)", text)

    for value in matches:
        value = clean_text(value)

        # On garde seulement les codes courts
        if 1 <= len(value) <= 20:
            forbidden_words = [
                "privatized",
                "former",
                "merged",
                "closed",
                "country",
                "only"
            ]

            if not any(word in value.lower() for word in forbidden_words):
                return value

    return None


def extract_operator_name(text):
    # Exemple :
    # "Société Nationale des Chemins de fer Français (SNCF)"
    # devient :
    # "Société Nationale des Chemins de fer Français"

    name = text.split("(")[0]

    # Si la ligne contient plusieurs infos séparées par des tirets,
    # on garde la première partie principale.
    name = name.split(" - ")[0]
    name = name.split(" – ")[0]
    name = name.split(" — ")[0]

    return clean_text(name)


# 📥 Requête vers la page web
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# 🎯 Chercher la section "National (state) railways"
target_h2 = None

for h2 in soup.find_all("h2"):
    title = h2.get_text(" ", strip=True)

    if "National (state) railways" in title:
        target_h2 = h2
        break

if target_h2 is None:
    raise Exception("Section 'National (state) railways' introuvable.")

# 📌 La liste <ul> juste après le titre contient les opérateurs nationaux
operator_list = target_h2.find_next("ul")

rows = []

for li in operator_list.find_all("li", recursive=False):
    text = clean_text(li.get_text(" ", strip=True))

    # Normaliser les tirets
    text = text.replace("—", "-").replace("–", "-")

    # On garde seulement les lignes du type : Country - Operator
    if " - " not in text:
        continue

    country_name, operator_text = text.split(" - ", 1)

    country_name = clean_text(country_name)
    operator_text = clean_text(operator_text)

    country_code = country_codes.get(country_name)

    # Si le pays n'existe pas dans notre dictionnaire, on ignore la ligne
    if country_code is None:
        continue

    operator_name = extract_operator_name(operator_text)
    operator_code = extract_operator_code(operator_text)

    if operator_name:
        rows.append({
            "operator_name": operator_name,
            "operator_code": operator_code,
            "country_code": country_code
        })


# 📊 Création du DataFrame
df_operator = pd.DataFrame(rows)

# 🧹 Suppression des lignes invalides
df_operator = df_operator.dropna(subset=["operator_name", "country_code"])

# 🧹 Suppression des doublons
df_operator = df_operator.drop_duplicates(subset=["operator_name", "country_code"])

# 🔁 Trier les données
df_operator = df_operator.sort_values(by=["country_code", "operator_name"])

# 📁 Dossier de sortie
output_dir = "data/raw/source_operator"
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, "operators.csv")

# 💾 Sauvegarde CSV
df_operator.to_csv(output_file, index=False, encoding="utf-8")

print("✔ CSV créé avec succès :", output_file)
print("Nombre d'opérateurs récupérés :", len(df_operator))
print(df_operator.head())