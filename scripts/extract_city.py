import pandas as pd
import os

# 📁 chemin du fichier TXT GeoNames
input_file = "data/raw/source_city/cities15000.txt"

# 📌 colonnes GeoNames (OBLIGATOIRE car fichier sans header)
columns = [
    "geonameid",
    "name",
    "ascii_name",
    "alternate_names",
    "latitude",
    "longitude",
    "feature_class",
    "feature_code",
    "country_code",
    "cc2",
    "admin1",
    "admin2",
    "admin3",
    "admin4",
    "population",
    "elevation",
    "dem",
    "timezone",
    "modification_date"
]

# 📥 lecture du fichier (TAB separated)
df = pd.read_csv(input_file, sep="\t", header=None, names=columns)

# 🎯 sélection des colonnes utiles pour ton projet
df_city = df[[
    "geonameid",
    "name",
    "country_code",
    "latitude",
    "longitude",
    "population"
]]

# 🔁 renommer selon ton MCD
df_city = df_city.rename(columns={
    "geonameid": "city_id",
    "name": "city_name"
})

# 🧹 suppression lignes invalides
df_city = df_city.dropna(subset=["city_id", "city_name", "country_code"])

# 📁 dossier de sortie
output_dir = "data/raw/source_city"
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, "cities.csv")

# 💾 sauvegarde CSV
df_city.to_csv(output_file, index=False, encoding="utf-8")

print("✔ CSV créé avec succès :", output_file)
print(df_city.head())