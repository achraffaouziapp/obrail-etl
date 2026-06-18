import pandas as pd
import os

# Données de référence pour la table TRAIN_TYPE
train_types = [
    {"type_name": "DAY"},
    {"type_name": "NIGHT"},
    {"type_name": "HIGH_SPEED"},
    {"type_name": "INTERCITY"},
    {"type_name": "REGIONAL"},
    {"type_name": "UNKNOWN"}
]

# Création DataFrame
df_train_type = pd.DataFrame(train_types)

# Suppression des doublons
df_train_type = df_train_type.drop_duplicates(subset=["type_name"])

# Nettoyage texte
df_train_type["type_name"] = df_train_type["type_name"].str.strip().str.upper()

# Dossier de sortie
output_dir = "data/raw/source_train_type"
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, "train_types.csv")

# Sauvegarde CSV
df_train_type.to_csv(output_file, index=False, encoding="utf-8")

print("✔ CSV créé avec succès :", output_file)
print(df_train_type)