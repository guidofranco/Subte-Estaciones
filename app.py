import streamlit as st
import pandas as pd
import pydeck
import psycopg2

conn = psycopg2.connect('host=localhost dbname=subte user=postgres password=milo')
cur = conn.cursor()
cur.execute("""
SELECT anio, estacion, long, lat, total
FROM (
SELECT anio, estacion, sum(total) as total
FROM pases
GROUP BY anio, estacion
ORDER BY anio) totales
INNER JOIN estaciones on estaciones.nombre = totales.estacion
""")

totales = cur.fetchall()

totales = pd.DataFrame(totales, columns=['anio', 'estacion', 'long', 'lat', 'total'], dtype='int')

year = st.sidebar.slider(
	'Seleccione un año',
	min_value = 2014,
	max_value = 2019)

month = st.sidebar.slider(
	'Seleccione un mes',
	min_value=1,
	max_value=12)

filtered = totales[totales.anio == year]

column_layer = pydeck.Layer(
    "ColumnLayer",
    data=filtered,
    get_position=["long", "lat"],
    get_elevation="total",
    elevation_scale=0.001,
    get_fill_color=['total/50000 + 50'],
    radius=100,
    pickable=True,
    auto_highlight=True,
)

view = pydeck.data_utils.compute_view(totales[['long', 'lat']])
view.zoom = 11
view.pitch = 45

deck = pydeck.Deck(
	column_layer, initial_view_state=view,
	tooltip={"text": "Estación: {estacion}\n Cant. de pasajeros: {total}"})

st.title('Cantidad de pasajeros por estación')
st.pydeck_chart(deck)
st.write(filtered[['estacion', 'total']])