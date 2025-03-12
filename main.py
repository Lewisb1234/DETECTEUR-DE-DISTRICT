import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Surveillance des Épidémies de Rougeole", layout="wide")

# Personnalisation de la sidebar
st.sidebar.markdown(
    """
    <style>
        .css-1d391kg {
            background-color: #f8f9fa !important;
        }
        .sidebar-title {
            font-size: 22px;
            font-weight: bold;
            color: #c62828;
            text-align: center;
        }
        .sidebar-item {
            font-size: 18px;
            padding: 10px;
            border-radius: 8px;
            transition: 0.3s;
            color: white;
            background: linear-gradient(90deg, #d32f2f, #c62828);
            text-align: center;
            margin: 5px 0;
        }
        .sidebar-item:hover {
            background: linear-gradient(90deg, #b71c1c, #880e4f);
            cursor: pointer;
        }
        .sidebar-logo {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 80%;
        }
        .sidebar-divider {
            height: 2px;
            background-color: #c62828;
            margin: 10px 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Affichage du logo et titre
st.sidebar.image("pev.png", use_container_width=True)  # Remplacez par le chemin réel du logo
st.sidebar.markdown('<div class="sidebar-title">📊 Navigation</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

# Options de navigation
pages = {
    "🏠 Accueil": "principal_page",
    "📈 Évolution des Cas épidémiques": "evolution_case",
    "📊 Statistiques globales et tendances": "statistiques",
    "🌍 Tableau de bord par province/district": "tableau_bord",
    "🔬 Analyse des Épidémies": "analyse_epidemies",
    "🗺️ Cartes des Foyers en Épidémies": "carte_epi",
    "🔮 Prédictions des Épidémies dans les régions": "predict_epid"
}

# Affichage des boutons améliorés
page = st.sidebar.radio("", list(pages.keys()), index=0)

# Charger la page correspondante
module_name = pages[page]
exec(f"from pages import {module_name}\n{module_name}.show()")
