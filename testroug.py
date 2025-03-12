import pandas as pd

# Charger les données
file_path = "Basedetectionepidemie.csv"
df = pd.read_csv(file_path)

# Standardiser les noms des colonnes
df.columns = df.columns.str.strip().str.lower()

# Normaliser les noms de district
df["districtofresidence"] = df["districtofresidence"].str.strip().str.upper()

# Convertir les dates
df["dateofonset"] = pd.to_datetime(df["dateofonset"], errors='coerce')

# Supprimer les lignes avec des dates invalides
df = df.dropna(subset=["dateofonset"])

# Vérifier les doublons
df = df.drop_duplicates()

# Afficher les années disponibles
for year in sorted(df["epiyear"].dropna().unique()):
    print(f"# Année {int(year)}")
    regions = df[df["epiyear"] == year]["provinceofresidence"].unique()
    for region in regions:
        print(f"## Région : {region}")
        districts = df[(df["epiyear"] == year) & (df["provinceofresidence"] == region)]["districtofresidence"].unique()
        for district in districts:
            print(f"### District : {district}")

# Regrouper les cas par district et semaine épidémiologique
cases_per_week = df.groupby(
    ["provinceofresidence", "districtofresidence", "epiyear", "semaine_epi"]).size().reset_index(name="case_count")


# Détecter les districts en épidémie
def detect_epidemic(district_cases, min_cases=1, min_weeks=4):
    epidemic_districts = []
    for (province, district), data in district_cases.groupby(["provinceofresidence", "districtofresidence"]):
        data = data.sort_values(by=["epiyear", "semaine_epi"])
        data["rolling_cases"] = data["case_count"].rolling(window=min_weeks).sum()
        if any(data["rolling_cases"] >= min_weeks):
            epidemic_districts.append((province, district))
    return epidemic_districts


epidemic_districts = detect_epidemic(cases_per_week)
print("Districts en épidémie :", epidemic_districts)

# Ajouter une colonne pour indiquer si un district est en épidémie
cases_per_week["epidemic"] = cases_per_week.apply(
    lambda row: (row["provinceofresidence"], row["districtofresidence"]) in epidemic_districts, axis=1)

# Sauvegarder les données mises à jour
updated_file_path = "epidemic_analysis.csv"
cases_per_week.to_csv(updated_file_path, index=False)
print(f"Données mises à jour sauvegardées dans {updated_file_path}")
