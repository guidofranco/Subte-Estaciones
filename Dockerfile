FROM python:3.7
EXPOSE 8501
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY app.py ./app.py
COPY estaciones-de-subte.csv ./estaciones-de-subte.csv
CMD streamlit run app.py
