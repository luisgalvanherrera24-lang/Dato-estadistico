
import streamlit as st
import requests
import pandas as pd
import os

# CONFIGURACIÓN SEGURA
API_KEY = os.getenv('API_SPORTS_KEY')
HEADERS = {'x-apisports-key': API_KEY}

st.set_page_config(page_title="Analizador de Parleys", layout="wide")
st.title("⚽ Analizador de Estadísticas Real-Time")

equipo_nombre = st.text_input("Ingresa el equipo (ej. Real Madrid):", "Real Madrid")

if st.button('Analizar Tendencias'):
    url_equipo = f"https://v3.football.api-sports.io/teams?name={equipo_nombre}"
    res_equipo = requests.get(url_equipo, headers=HEADERS).json()
    
    if res_equipo.get('response'):
        team_id = res_equipo['response'][0]['team']['id']
        url_stats = f"https://v3.football.api-sports.io/teams/statistics?season=2025&league=140&team={team_id}"
        res_stats = requests.get(url_stats, headers=HEADERS).json()
        
        if res_stats.get('response'):
            data = res_stats['response']
            stats_finales = [
                {"Mercado": "CORNERS (Promedio)", "Valor": data['corners']['avg']['total']},
                {"Mercado": "GOLES FAVOR (Promedio)", "Valor": data['goals']['for']['average']['total']},
                {"Mercado": "GOLES CONTRA (Promedio)", "Valor": data['goals']['against']['average']['total']}
            ]
            st.table(pd.DataFrame(stats_finales))
            st.success("¡Datos cargados!")
        else:
            st.error("No hay datos para esta liga.")
    else:
        st.error("Equipo no encontrado.")
