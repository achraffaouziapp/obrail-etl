import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

url = "https://www.geonames.org/countries/"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", {"class": "restable"})
rows = table.find_all("tr")

countries = []

for row in rows[1:]:
    cols = row.find_all("td")

    # sécurité structure GeoNames
    if len(cols) >= 4:
        country_code = cols[0].text.strip()   # ISO-3166 alpha2
        country_name = cols[4].text.strip()   # Country

        countries.append([country_code, country_name])

# création DataFrame avec ordre FIXE
df = pd.DataFrame(countries, columns=["country_code", "country_name"])

# dossier output
output_dir = "data/raw/source_country"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "countries.csv")

# sauvegarde CSV
df.to_csv(output_path, index=False, encoding="utf-8")

print("✔ CSV créé avec succès :", output_path)
print(df.head())