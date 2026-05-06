import streamlit as st
import requests
import pd
import os

# 1. CONFIGURACIÓN DE SEGURIDAD (Se conecta con los Secrets de Streamlit)
API_KEY = os.getenv('API_SPORTS_KEY')
HEADERS = {'x-apisports-key': API_KEY}

# Configuración de la página
st.set_page_config(page_title="Analizador de Parleys", layout="wide")
st.title("⚽ Analizador de Estadísticas Real-Time")
st.markdown("---")

# 2. ENTRADA DEL USUARIO
equipo_nombre = st.text_input("Escribe el nombre del equipo (en inglés, ej: Real Madrid, Liverpool, Bayern Munich):", "Real Madrid")

if st.button('🚀 ANALIZAR PARTIDO'):
    with st.spinner('Buscando datos en la web...'):
        # Paso A: Buscar el ID del equipo
        url_equipo = f"https://v3.football.api-sports.io/teams?name={equipo_nombre}"
        res_equipo = requests.get(url_equipo, headers=HEADERS).json()
        
        if res_equipo.get('response'):
            team_id = res_equipo['response'][0]['team']['id']
            nombre_real = res_equipo['response'][0]['team']['name']
            escudo = res_equipo['response'][0]['team']['logo']

            # Paso B: Traer estadísticas (Temporada 2025, Liga 140 - España como ejemplo)
            # Nota: Se puede ajustar la liga según el partido
            url_stats = f"https://v3.football.api-sports.io/teams/statistics?season=2025&league=140&team={team_id}"
            res_stats = requests.get(url_stats, headers
