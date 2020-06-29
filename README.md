## Pasajeros por estación de subte

Simple app hecha con [Streamlit](https://www.streamlit.io/) para visualizar la cantidad de pasajeros que circularon por estación de subte

### Datos

Los datos provienen de la plataforma de datos abiertos de CABA

Los datos de la cantidad de pasajeros provienen de esta [fuente](https://data.buenosaires.gob.ar/dataset/subte-viajes-molinetes). Comprenden el periodo 2014-2019 y fueron procesados previamente con PySpark. Los datos procesados se encuentran [aquí](https://gdostorage.blob.core.windows.net/gcontainer/molinetes.gzip), cabe aclarar que están comprimidos en formato parquet.

### Base de datos

Se trabaja con una base de datos local PostgreSQL.

En este repositorio se encuentran los archivos `.sql`, con el esquema y los datos de las tablas, para que pueda levantar localmente esta base de datos (están comprimidos).

### Ejecución

Se parte de que ya ha creado y cargado la base de datos empleando los archivos `.sql`

1. Clonar el repositorio.
2. Ubicarse en la carpeta de este proyecto.
3. Crear un entorno virtual, con el gestor de paquetes y entornos [conda](https://docs.conda.io/en/latest/), de la siguiente forma `conda create -n app_env python=3.8`
4. Luego, `conda activate app_env`.
5. A continuación, `streamlit run app.py`.
6. Acceder a la app en `localhost:8501`.
