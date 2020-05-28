import streamlit as st
import pandas as pd
import pydeck

@st.cache
def load_data():
	df =  pd.read_parquet(DATA_URL)
	df.fecha = pd.to_datetime(df.fecha)
	return df

@st.cache
def filter_data(df, year, month):
	return df.loc[year, month]

@st.cache
def load_stations():
	stations = pd.read_csv('estaciones-de-subte.csv', usecols=['estacion'])
	return stations.estacion.unique()

@st.cache()
def filter_station(df, station_name):
	return df[df.estacion == station_name]

@st.cache
def group_data(df):
	df = df.groupby([
			df.fecha.dt.year, df.fecha.dt.month, df.estacion
			]) \
		.agg({'cantidad': 'sum'})

	return df

DATA_URL = 'https://gdostorage.blob.core.windows.net/gcontainer/molinetes.gzip'

# STATION_NAMES = load_stations()

estaciones = pd.read_csv('estaciones-de-subte.csv',
						usecols=['estacion', 'lat', 'long'])
estaciones.drop_duplicates('estacion', inplace=True, ignore_index=True)

year = st.sidebar.slider(
	'Seleccione un año',
	min_value = 2014,
	max_value = 2019)

month = st.sidebar.slider(
	'Seleccione un mes',
	min_value=1,
	max_value=12)

#station = st.sidebar.selectbox(
#	label = 'Seleccione una estación',
#	options=STATION_NAMES)

df = load_data()

grouped = group_data(df)
filtered = filter_data(grouped, year, month)

joined = pd.merge(filtered, estaciones, on='estacion', how='inner')

column_layer = pydeck.Layer(
    "ColumnLayer",
    data=joined,
    get_position=["long", "lat"],
    get_elevation="cantidad",
    elevation_scale=0.01,
    get_fill_color=['cantidad/10000 + 50'],
    radius=100,
    pickable=True,
    auto_highlight=True,
)

view = pydeck.data_utils.compute_view(joined[['long', 'lat']])
view.zoom = 11
view.pitch = 45

deck = pydeck.Deck(
	column_layer, initial_view_state=view,
	tooltip={"text": "Estación: {estacion}\n Cant. de pasajeros: {cantidad}"})

st.title('Cantidad de pasajeros por estación')
st.pydeck_chart(deck)
st.write(joined[['estacion', 'cantidad']])