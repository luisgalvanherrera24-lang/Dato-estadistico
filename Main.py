import streamlit as st
import requests
import pandas as pd
import os

# Configuración
API_KEY = os.getenv('API_SPORTS_KEY')
HEADERS = {'x-apisports-key': API_KEY}

st.set_page_config(page_title="Analizador Pro", layout="wide")
st.title("⚽ Buscador de Estadísticas")

col1, col2 = st.columns(2)
with col1:
    eq1 = st.text_input("Local:", "Real Madrid")
with col2:
    eq2 = st.text_input("Visitante:", "Barcelona")

def buscar_stats(nombre):
    res = requests.get(f"https://v3.football.api-sports.io/teams?search={nombre}", headers=HEADERS).json()
    if not res.get('response'): return None
    t_id = res['response'][0]['team']['id']
    
    # Probamos temporadas recientes
    for year in [2025, 2024]:
        l_res = requests.get(f"https://v3.football.api-sports.io/leagues?team={t_id}&current=true", headers=HEADERS).json()
        if not l_res.get('response'): continue
        
        l_id = l_res['response'][0]['league']['id']
        s_res = requests.get(f"https://v3.football.api-sports.io/teams/statistics?season={year}&league={l_id}&team={t_id}", headers=HEADERS).json()
        
        if s_res.get('response'):
            d = s_res['response']
            # Protección contra datos vacíos (KeyError)
            corners = d.get('corners', {}).get('avg', {}).get('total', 0)
            goles = d.get('goals', {}).get('for', {}).get('average', {}).get('total', 0)
            return {"Corners": corners, "Goles": goles}
    return None

if st.button('🔍 CARGAR DATOS'):
    with st.spinner('Consultando...'):
        d1 = buscar_stats(eq1)
        d2 = buscar_stats(eq2)
        
        if d1 and d2:
            df = pd.DataFrame([
                {"Mercado": "Córners (Avg)", eq1: d1['Corners'], eq2: d2['Corners']},
                {"Mercado": "Goles (Avg)", eq1: d1['Goles'], eq2: d2['Goles']}
            ])
            st.table(df)
            st.success("¡Datos cargados!")
        else:
            st.error("No se encontraron datos estadísticos. Prueba con otro nombre.")
