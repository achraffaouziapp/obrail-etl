import pandas as pd
import os
import re

# 📁 fichier source brut créé par extract_operator.py
input_file = "data/raw/source_operator/operators.csv"

# 📁 dossier de sortie pour les données nettoyées
output_dir = "data/processed"
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, "operators_clean.csv")


def clean_text(value):
    if pd.isna(value):
        return None

    value = str(value)

    # supprimer les références comme [1], [2]
    value = re.sub(r"\[\d+\]", "", value)

    # remplacer plusieurs espaces par un seul
    value = re.sub(r"\s+", " ", value)

    # supprimer les espaces au début et à la fin
    value = value.strip()

    if value == "":
        return None

    return value


# 📥 lecture du fichier operators.csv
df = pd.read_csv(input_file)

# 🎯 garder seulement les colonnes utiles pour le MPD
df_operator = df[[
    "operator_name",
    "operator_code",
    "country_code"
]].copy()

# 🧹 nettoyage des textes
df_operator["operator_name"] = df_operator["operator_name"].apply(clean_text)
df_operator["operator_code"] = df_operator["operator_code"].apply(clean_text)
df_operator["country_code"] = df_operator["country_code"].apply(clean_text)

# 🔁 mettre les codes pays en majuscules
df_operator["country_code"] = df_operator["country_code"].str.upper()

# 🧹 supprimer les lignes invalides
df_operator = df_operator.dropna(subset=["operator_name", "country_code"])

# 🧹 garder seulement les codes pays de 2 lettres
df_operator = df_operator[
    df_operator["country_code"].str.match(r"^[A-Z]{2}$", na=False)
]

# 🧹 supprimer les doublons
df_operator = df_operator.drop_duplicates(
    subset=["operator_name", "country_code"]
)

# 🔁 trier les données
df_operator = df_operator.sort_values(
    by=["country_code", "operator_name"]
)

# 💾 sauvegarde du fichier nettoyé
df_operator.to_csv(output_file, index=False, encoding="utf-8")

print("✔ OPERATOR nettoyé avec succès :", output_file)
print("Nombre de lignes :", len(df_operator))
print(df_operator.head())