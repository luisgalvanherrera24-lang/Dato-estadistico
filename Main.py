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
    # Paso 1: Buscar el equipo
    res = requests.get(f"https://v3.football.api-sports.io/teams?search={nombre}", headers=HEADERS).json()
    if not res.get('response'): return None
    
    t_id = res['response'][0]['team']['id']
    
    # Paso 2: Intentar traer estadísticas (Probamos 2024 y 2023 por si acaso)
    for year in [2025, 2024, 2023]:
        # Buscamos la liga principal del equipo
        l_res = requests.get(f"https://v3.football.api-sports.io/leagues?team={t_id}&current=true", headers=HEADERS).json()
        if not l_res.get('response'): continue
        
        l_id = l_res['response'][0]['league']['id']
        s_res = requests.get(f"https://v3.football.api-sports.io/teams/statistics?season={year}&league={l_id}&team={t_id}", headers=HEADERS).json()
        
        if s_res.get('response') and s_res['response']['corners']['avg']['total'] is not None:
            d = s_res['response']
            return {
                "Corners": d['corners']['avg']['total'],
                "Goles": d['goals']['for']['average']['total']
            }
    return None

if st.button('🔍 CARGAR DATOS'):
    with st.spinner('Consultando base de datos...'):
        d1 = buscar_stats(eq1)
        d2 = buscar_stats(eq2)
        
        if d1 and d2:
            df = pd.DataFrame([
                {"Mercado": "Promedio Córners", eq1: d1['Corners'], eq2: d2['Corners']},
                {"Mercado": "Promedio Goles", eq1: d1['Goles'], eq2: d2['Goles']}
            ])
            st.table(df)
            st.success("¡Datos cargados!")
        else:
            st.error("No se encontraron datos. Verifica que el nombre esté bien escrito (ej: Man City).")
import streamlit as st
import requests
import pandas as pd
import os

# Configuración
API_KEY = os.getenv('API_SPORTS_KEY')
HEADERS = {'x-apisports-key': API_KEY}

st.set_page_config(page_title="Analizador de Parleys", layout="wide")
st.title("⚽ Tu Analizador de Parleys")
st.write("Solo escribe los nombres y yo busco los promedios.")

# FILA PARA LOS DOS EQUIPOS
col1, col2 = st.columns(2)

with col1:
    equipo1 = st.text_input("Equipo Local:", "Real Madrid")
with col2:
    equipo2 = st.text_input("Equipo Visitante:", "Barcelona")

def obtener_data(nombre):
    # Paso 1: Buscar ID del equipo
    url = f"https://v3.football.api-sports.io/teams?search={nombre}"
    res = requests.get(url, headers=HEADERS).json()
    if res.get('response'):
        t_id = res['response'][0]['team']['id']
        # Paso 2: Traer estadísticas (usamos temporada 2024 que está completa)
        # Probamos con una liga común, si no, busca la liga actual
        url_s = f"https://v3.football.api-sports.io/teams/statistics?season=2024&league=140&team={t_id}"
        stats = requests.get(url_s, headers=HEADERS).json()
        if stats.get('response'):
            d = stats['response']
            return {
                "Corners": d['corners']['avg']['total'],
                "Goles": d['goals']['for']['average']['total'],
                "Tarjetas": d['cards']['yellow']['0-15']['total'] or "N/A" # Ejemplo de tarjetas
            }
    return None

if st.button('🔥 LLENAR ANÁLISIS'):
    data1 = obtener_data(equipo1)
    data2 = obtener_data(equipo2)
    
    if data1 and data2:
        tabla = [
            {"Mercado": "Promedio Córners", equipo1: data1['Corners'], equipo2: data2['Corners']},
            {"Mercado": "Promedio Goles", equipo1: data1['Goles'], equipo2: data2['Goles']}
        ]
        st.table(pd.DataFrame(tabla))
        st.success("¡Análisis completado para tu parley!")
    else:
        st.error("No pude encontrar datos de uno de los equipos. Revisa que estén bien escritos.")

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
