import streamlit as st
import requests
import pandas as pd
import os

# Configuración
API_KEY = os.getenv('API_SPORTS_KEY')
HEADERS = {'x-apisports-key': API_KEY}

st.set_page_config(page_title="Analizador Pro Luis", layout="wide")
st.title("⚽ Analizador de Estadísticas")

# --- PASO 1: LOS INPUTS (ENTRADAS) ---
# Aquí es donde escribes los equipos. Les puse llaves únicas para evitar el error.
c1, c2 = st.columns(2)
with c1:
    eq_local = st.text_input("Equipo Local:", value="Real Madrid", key="L_PRO_2026")
with c2:
    eq_visit = st.text_input("Equipo Visitante:", value="Barcelona", key="V_PRO_2026")

def buscar_stats(nombre):
    try:
        res = requests.get(f"https://v3.football.api-sports.io/teams?search={nombre}", headers=HEADERS).json()
        if not res.get('response'): return None
        t_id = res['response'][0]['team']['id']
        
        l_res = requests.get(f"https://v3.football.api-sports.io/leagues?team={t_id}&current=true", headers=HEADERS).json()
        if not l_res.get('response'): return None
        l_id = l_res['response'][0]['league']['id']

        # --- PASO 2: LA TEMPORADA ---
        # Usamos 2025 para tener los datos más frescos
        s_res = requests.get(f"https://v3.football.api-sports.io/teams/statistics?season=2025&league={l_id}&team={t_id}", headers=HEADERS).json()
        
        if s_res.get('response'):
            d = s_res['response']
            corn = d.get('corners', {}).get('avg', {}).get('total', 0)
            gol = d.get('goals', {}).get('for', {}).get('average', {}).get('total', 0)
            return {"C": corn, "G": gol}
    except:
        return None
    return None

# --- PASO 3: EL BOTÓN DE ANÁLISIS ---
if st.button('🔥 ANALIZAR PARTIDO', key="BOTON_PRINCIPAL"):
    with st.spinner('Buscando datos en la API...'):
        d1 = buscar_stats(eq_local)
        d2 = buscar_stats(eq_visit)
        
        if d1 and d2:
            df = pd.DataFrame([
                {"Mercado": "Córners (Promedio)", eq_local: d1['C'], eq_visit: d2['C']},
                {"Mercado": "Goles (Promedio)", eq_local: d1['G'], eq_visit: d2['G']}
            ])
            st.table(df)
            
            # Un pequeño cálculo extra para tus parleys
            total_c = float(d1['C']) + float(d2['C'])
            st.info(f"💡 Promedio combinado de córners: {total_c:.2f}")
        else:
            st.error("No encontré datos. Asegúrate de que el nombre del equipo esté en inglés.")
