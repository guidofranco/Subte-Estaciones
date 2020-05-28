## Pasajeros por estación de subte

Simple app hecha con [Streamlit](https://www.streamlit.io/) para visualizar la cantidad de pasajeros que circularon por estación de subte

### Datos

Los datos provienen de la plataforma de datos abiertos de CABA

Los datos de la cantidad de pasajeros provienen de esta [fuente](https://data.buenosaires.gob.ar/dataset/subte-viajes-molinetes). Comprenden el periodo 2014-2019 y fueron procesado previamente con PySpark. Los datos procesados utilizados para la visualización se encuentran [aquí](https://gdostorage.blob.core.windows.net/gcontainer/molinetes.gzip), cabe aclarar que están comprimidos en formato parquet.

### Entorno

Se puede replicar este trabajo en un máquina local de la siguiente forma:

1. Clonar el repositorio
2. Ubicarse en la carpeta de este proyecto
3. Ejecutar en la consola `docker build -f Dockerfile  -t app:latest .`
4. Luego ejecutar `docker run -it -p 8501:8501 app:latest`
5. Acceder a la app en `localhost:8501`
