import streamlit as st
import requests
import pandas as pd
import os

# Configuración
API_KEY = os.getenv('API_SPORTS_KEY')
HEADERS = {'x-apisports-key': API_KEY}

st.set_page_config(page_title="Analizador Pro Luis", layout="wide")
st.title("⚽ Analizador de Estadísticas")

# Nombres de campos totalmente nuevos para forzar la limpieza
c1, c2 = st.columns(2)
with c1:
    eq_local = st.text_input("Equipo Local:", value="Real Madrid", key="L1")
with c2:
    eq_visit = st.text_input("Equipo Visitante:", value="Barcelona", key="V1")

def buscar_stats(nombre):
    try:
        res = requests.get(f"https://v3.football.api-sports.io/teams?search={nombre}", headers=HEADERS).json()
        if not res.get('response'): return None
        t_id = res['response'][0]['team']['id']
        
        l_res = requests.get(f"https://v3.football.api-sports.io/leagues?team={t_id}&current=true", headers=HEADERS).json()
        if not l_res.get('response'): return None
        l_id = l_res['response'][0]['league']['id']

        s_res = requests.get(f"https://v3.football.api-sports.io/teams/statistics?season=2024&league={l_id}&team={t_id}", headers=HEADERS).json()
        
        if s_res.get('response'):
            d = s_res['response']
            corn = d.get('corners', {}).get('avg', {}).get('total', 0)
            gol = d.get('goals', {}).get('for', {}).get('average', {}).get('total', 0)
            return {"C": corn, "G": gol}
    except:
        return None
    return None

if st.button('🔥 ANALIZAR PARTIDO', key="B1"):
    with st.spinner('Buscando datos...'):
        d1 = buscar_stats(eq_local)
        d2 = buscar_stats(eq_visit)
        
        if d1 and d2:
            df = pd.DataFrame([
                {"Mercado": "Córners (Promedio)", eq_local: d1['C'], eq_visit: d2['C']},
                {"Mercado": "Goles (Promedio)", eq_local: d1['G'], eq_visit: d2['G']}
            ])
            st.table(df)
        else:
            st.error("Revisa la llave API en Secrets o el nombre de los equipos.")
import streamlit as st
import requests
import pandas as pd
import os

# Configuración
API_KEY = os.getenv('API_SPORTS_KEY')
HEADERS = {'x-apisports-key': API_KEY}

st.set_page_config(page_title="Analizador Pro", layout="wide")
st.title("⚽ Mi Analizador de Parleys")

# Campos de texto con nombres únicos para evitar el error de la foto
col1, col2 = st.columns(2)
with col1:
    eq1 = st.text_input("Local:", value="Real Madrid", key="local_input")
with col2:
    eq2 = st.text_input("Visitante:", value="Barcelona", key="visitante_input")

def buscar_stats(nombre):
    try:
        res = requests.get(f"https://v3.football.api-sports.io/teams?search={nombre}", headers=HEADERS).json()
        if not res.get('response'): return None
        t_id = res['response'][0]['team']['id']
        
        l_res = requests.get(f"https://v3.football.api-sports.io/leagues?team={t_id}&current=true", headers=HEADERS).json()
        if not l_res.get('response'): return None
        l_id = l_res['response'][0]['league']['id']

        s_res = requests.get(f"https://v3.football.api-sports.io/teams/statistics?season=2024&league={l_id}&team={t_id}", headers=HEADERS).json()
        
        if s_res.get('response'):
            d = s_res['response']
            corners = d.get('corners', {}).get('avg', {}).get('total', 0)
            goles = d.get('goals', {}).get('for', {}).get('average', {}).get('total', 0)
            return {"Corners": corners, "Goles": goles}
    except:
        return None
    return None

if st.button('🔍 CARGAR DATOS', key="boton_analizar"):
    with st.spinner('Analizando...'):
        d1 = buscar_stats(eq1)
        d2 = buscar_stats(eq2)
        
        if d1 and d2:
            df = pd.DataFrame([
                {"Mercado": "Promedio Córners", eq1: d1['Corners'], eq2: d2['Corners']},
                {"Mercado": "Promedio Goles", eq1: d1['Goles'], eq2: d2['Goles']}
            ])
            st.table(df)
            st.success("¡Análisis completado!")
        else:
            st.error("No hay datos. Revisa la llave API en Secrets.")
import streamlit as st
import requests
import pandas as pd
import os

# Configuración
API_KEY = os.getenv('API_SPORTS_KEY')
HEADERS = {'x-apisports-key': API_KEY}

st.set_page_config(page_title="Analizador Pro", layout="wide")
st.title("⚽ Tu Analizador de Parleys")

col1, col2 = st.columns(2)
with col1:
    eq1 = st.text_input("Local:", "Real Madrid")
with col2:
    eq2 = st.text_input("Visitante:", "Barcelona")

def buscar_stats(nombre):
    try:
        # 1. Buscar equipo
        res = requests.get(f"https://v3.football.api-sports.io/teams?search={nombre}", headers=HEADERS).json()
        if not res.get('response'): return None
        t_id = res['response'][0]['team']['id']
        
        # 2. Buscar liga actual
        l_res = requests.get(f"https://v3.football.api-sports.io/leagues?team={t_id}&current=true", headers=HEADERS).json()
        if not l_res.get('response'): return None
        l_id = l_res['response'][0]['league']['id']

        # 3. Traer estadísticas (Temporada 2024 que es la más estable)
        s_res = requests.get(f"https://v3.football.api-sports.io/teams/statistics?season=2024&league={l_id}&team={t_id}", headers=HEADERS).json()
        
        if s_res.get('response'):
            d = s_res['response']
            # Usamos .get() para que si no existe el dato, no salga el error rojo
            corners = d.get('corners', {}).get('avg', {}).get('total', "0")
            goles = d.get('goals', {}).get('for', {}).get('average', {}).get('total', "0")
            return {"Corners": corners, "Goles": goles}
    except:
        return None
    return None

if st.button('🔍 CARGAR DATOS'):
    with st.spinner('Analizando...'):
        d1 = buscar_stats(eq1)
        d2 = buscar_stats(eq2)
        
        if d1 and d2:
            df = pd.DataFrame([
                {"Mercado": "Promedio Córners", eq1: d1['Corners'], eq2: d2['Corners']},
                {"Mercado": "Promedio Goles", eq1: d1['Goles'], eq2: d2['Goles']}
            ])
            st.table(df)
            st.success("¡Análisis listo!")
        else:
            st.error("No encontré datos. Revisa si la llave API está bien puesta en Secrets.")
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
