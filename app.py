import streamlit as st
import pandas as pd
import pydeck
import psycopg2
import json

def connect_db(credentials_dict):
    return psycopg2.connect(f'host={credentials_dict["host"]} \
                        dbname={credentials_dict["dbname"]} \
                        user={credentials_dict["user"]} \
                        password={credentials_dict["password"]}')

def load_passes_data(cursor):
    cursor.execute("""
    SELECT anio, mes, estacion, totales.linea, long, lat, total
    FROM (
    SELECT anio, mes, estacion, linea, sum(total) as total
    FROM pases
    GROUP BY anio, mes, estacion, linea
    ORDER BY anio, mes, estacion) totales
    INNER JOIN estaciones on estaciones.nombre = totales.estacion
    AND estaciones.linea = totales.linea
    """)
    return cursor.fetchall()

def load_passes_per_day(connection_string, month, year):
    cur.execute(f"""
    SELECT dia_mes, sum(total) as total
    FROM pases
    WHERE anio = {year} AND mes = {month} AND estacion = '{estacion}'
    GROUP BY dia_mes
    ORDER BY dia_mes
    """)
    return cur.fetchall()

def load_subway_lines(cursor):
    cursor.execute("""
    SELECT distinct(linea)
    FROM estaciones
    ORDER BY linea
    """)
    return cur.fetchall()

def load_subway_stations(cursor, subway_line):
    cursor.execute(f"""
    SELECT nombre
    FROM estaciones
    WHERE linea = '{linea}'
    """)
    return cursor.fetchall()   

def filter_passes_data():
    pass
# Database connection
with open('db_credentials.json') as credentials_file:
    credentials_dict = json.load(credentials_file)
conn = connect_db(credentials_dict)
cur = conn.cursor()

totales = load_passes_data(cur)
totales = pd.DataFrame(totales, \
                    columns=['anio', 'mes', 'estacion', 'linea', 'long', 'lat', 'total'], \
                    dtype='int')

st.title('Cantidad de pasajeros por estación')
year = st.slider(
	'Seleccione un año',
	min_value = 2014,
	max_value = 2019)
month = st.slider(
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

lineas = load_subway_lines(cur)
lineas = [l[0] for l in lineas]
linea = st.selectbox('Linea', lineas)
estaciones_por_linea = load_subway_stations(cur, linea)
estaciones_por_linea = [_[0] for _ in estaciones_por_linea]
estacion = st.selectbox("Estacion", estaciones_por_linea)

result = load_passes_per_day(cur, month, year)
result = pd.DataFrame(result, columns=['dia_del_mes', 'total'], dtype='int')

st.vega_lite_chart( \
    result, \
    {
        "mark": {"type": "line"},
        "encoding": {
            "x": {"field":"dia_del_mes", "type": "ordinal"},
            "y": {"field":"total", "type": "quantitative"}
        }
    })