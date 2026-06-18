import pandas as pd
import os
import re

# 📁 fichier source brut créé par extract_train_type.py
input_file = "data/raw/source_train_type/train_types.csv"

# 📁 dossier de sortie pour les données nettoyées
output_dir = "data/processed"
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, "train_types_clean.csv")


def clean_text(value):
    if pd.isna(value):
        return None

    value = str(value)

    # remplacer plusieurs espaces par un seul
    value = re.sub(r"\s+", " ", value)

    # supprimer les espaces au début et à la fin
    value = value.strip()

    if value == "":
        return None

    return value


# 📥 lecture du fichier train_types.csv
df = pd.read_csv(input_file)

# 🎯 garder seulement la colonne utile pour le MPD
df_train_type = df[["type_name"]].copy()

# 🧹 nettoyage du texte
df_train_type["type_name"] = df_train_type["type_name"].apply(clean_text)

# 🔁 mettre en majuscules
df_train_type["type_name"] = df_train_type["type_name"].str.upper()

# 🔁 remplacer les espaces par _
df_train_type["type_name"] = df_train_type["type_name"].str.replace(" ", "_")

# 🧹 supprimer les lignes vides
df_train_type = df_train_type.dropna(subset=["type_name"])

# ✅ types autorisés dans notre projet
allowed_types = [
    "DAY",
    "NIGHT",
    "HIGH_SPEED",
    "INTERCITY",
    "REGIONAL",
    "UNKNOWN"
]

# 🧹 garder seulement les types autorisés
df_train_type = df_train_type[
    df_train_type["type_name"].isin(allowed_types)
]

# 🧹 supprimer les doublons
df_train_type = df_train_type.drop_duplicates(subset=["type_name"])

# 🔁 garder un ordre logique
df_train_type["type_order"] = df_train_type["type_name"].apply(
    lambda x: allowed_types.index(x)
)

df_train_type = df_train_type.sort_values("type_order")
df_train_type = df_train_type.drop(columns=["type_order"])

# 💾 sauvegarde du fichier nettoyé
df_train_type.to_csv(output_file, index=False, encoding="utf-8")

print("✔ TRAIN_TYPE nettoyé avec succès :", output_file)
print("Nombre de lignes :", len(df_train_type))
print(df_train_type)