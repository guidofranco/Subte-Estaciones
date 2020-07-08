import streamlit as st
import pandas as pd
import pydeck
import pyodbc
import json

def connect_db():
    with open('db_credentials.json') as credentials_file:
        credentials_dict = json.load(credentials_file)
    conn_str = f"DRIVER={credentials_dict['driver']};SERVER={credentials_dict['server']};\
        PORT=1433;DATABASE={credentials_dict['database']};UID={credentials_dict['username']};\
        PWD={credentials_dict['password']}"
    return pyodbc.connect(conn_str)

@st.cache
def load_passes_data():
    cursor.execute("""
    SELECT anio, mes, estacion, totales.linea, long, lat, total
    FROM (
    SELECT anio, mes, estacion, linea, sum(total) as total
    FROM pases
    GROUP BY anio, mes, estacion, linea) totales
    INNER JOIN estaciones on estaciones.nombre = totales.estacion
    AND estaciones.linea = totales.linea
    """)
    return cursor.fetchall()

@st.cache
def load_passes_per_day(month, year, station):
    cursor.execute(f"""
    SELECT dia_mes, sum(total) as total
    FROM pases
    WHERE anio = {year} AND mes = {month}
    AND estacion = '{station}'
    GROUP BY dia_mes
    ORDER BY dia_mes
    """)
    return cursor.fetchall()

@st.cache
def load_subway_lines():
    cursor.execute("""
    SELECT distinct(linea)
    FROM estaciones
    ORDER BY linea
    """)
    return cursor.fetchall()

@st.cache
def load_subway_stations(subway_line):
    cursor.execute(f"""
    SELECT nombre
    FROM estaciones
    WHERE linea = '{subway_line}'
    """)
    return cursor.fetchall()   

def filter_passes_data():
    pass

conn = connect_db()
cursor = conn.cursor()

totales = load_passes_data()
totales = [tuple(row) for row in totales]
totales = pd.DataFrame(totales, \
                    columns=['anio', 'mes', 'estacion', 'linea', 'long', 'lat', 'total'])

st.title('Cantidad de pasajeros por estación')

year = st.sidebar.slider(
	'Seleccione un año',
	min_value = 2014,
	max_value = 2019)
month = st.sidebar.slider(
	'Seleccione un mes',
	min_value=1,
	max_value=12)
filtered = totales[(totales.anio == year) & (totales.mes == month)]

column_layer = pydeck.Layer(
    "ColumnLayer",
    data=filtered,
    get_position=["long", "lat"],
    get_elevation="total",
    elevation_scale=0.01,
    get_fill_color=['total/5000 + 50'],
    radius=100,
    pickable=True,
    auto_highlight=True,
)

view = pydeck.data_utils.compute_view(totales[['long', 'lat']])
view.zoom = 11
view.pitch = 45

deck = pydeck.Deck(
	column_layer, initial_view_state=view,
	tooltip={"text": "Estación: {estacion}\n Linea: {linea}\n Cant. de pasajeros: {total}"})

st.pydeck_chart(deck)

lineas = load_subway_lines()
lineas = [linea[0] for linea in lineas]
linea = st.sidebar.selectbox('Linea', lineas)
estaciones_por_linea = load_subway_stations(linea)
estaciones_por_linea = [estacion[0] for estacion in estaciones_por_linea]
estacion = st.sidebar.selectbox("Estacion", estaciones_por_linea)

result = load_passes_per_day(month, year, estacion)
result = [tuple(row) for row in result]
result = pd.DataFrame(result, columns=['dia_del_mes', 'total'])
# st.write(result)

st.vega_lite_chart( \
    result, \
    {
        "mark": {"type": "line"},
        "encoding": {
            "x": {"field":"dia_del_mes", "type": "ordinal"},
            "y": {"field":"total", "type": "quantitative"}
        }
    })

cursor.close()