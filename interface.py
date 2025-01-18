import streamlit as st
import requests

# Appliquer le style CSS pour ajouter une image en fond
page_bg_img = '''
<style>
.stApp {
    background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQglXx-fSEEdexUw7yi1y89mvLYuVdKFXpVHA&s");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Titre de l'application
st.title("Prédiction de la qualité du vin")
st.markdown("""
Ajustez les paramètres chimiques ci-dessous pour prédire la qualité d'un vin.
""")

# Organisation en colonnes pour économiser de l'espace
col1, col2, col3 = st.columns(3)

with col1:
    fixed_acidity = st.slider("Acidité fixe", 4.0, 16.0, 7.4)
    volatile_acidity = st.slider("Acidité volatile", 0.1, 1.5, 0.7)
    citric_acid = st.slider("Acide citrique", 0.0, 1.0, 0.0)
    residual_sugar = st.slider("Sucre résiduel", 0.5, 20.0, 1.9)

with col2:
    chlorides = st.slider("Chlorures", 0.01, 0.1, 0.076)
    free_sulfur_dioxide = st.slider("SO2 libre", 1, 70, 11)
    total_sulfur_dioxide = st.slider("SO2 total", 6, 300, 34)
    density = st.slider("Densité", 0.9900, 1.0050, 0.9978)

with col3:
    pH = st.slider("pH", 2.5, 4.5, 3.51)
    sulphates = st.slider("Sulfates", 0.3, 2.0, 0.56)
    alcohol = st.slider("Alcool", 8.0, 15.0, 10.0)

# Bouton pour effectuer la prédiction
if st.button("Prédire la qualité"):
    # Données d'entrée sous forme de liste
    input_data = [
        fixed_acidity / 10**2, volatile_acidity / 10, citric_acid / 10, residual_sugar / 10**2, chlorides,
        free_sulfur_dioxide / 10**3, total_sulfur_dioxide / 10**3, density / 10, pH / 10, sulphates / 10, alcohol / 10**2
    ]

    # Préparer les données pour l'API
    payload = {
        "data": [input_data]
    }
    
    # URL du point de terminaison (modifiez cette URL par votre endpoint déployé)
    api_url = "https://mlw-project-uftgl.westeurope.inference.ml.azure.com/score"

    # Header avec Authorization Bearer
    headers = {
        "Authorization": f"Bearer 798nu8qmKNKq2HOu9M11CYKBmSG6ZwXF",
        "Content-Type": "application/json"
    }
    
    # Appel à l'API
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        
        # Vérifier le statut de la réponse
        if response.status_code == 200:
            prediction = response.json()
            st.success(f"Qualité prédite : {prediction[0][0] * 6 + 3}")
        else:
            st.error(f"Erreur lors de l'appel API : {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Erreur : {e}")
