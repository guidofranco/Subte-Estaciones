FROM python:3.8-slim
EXPOSE 8501
RUN \
  apt-get update && \
  apt-get install -y curl build-essential unixodbc-dev g++ apt-transport-https
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA='Y' apt-get install -y msodbcsql17
RUN pip install pyodbc streamlit
CMD streamlit run simple_app.py
COPY simple_app.py /simple_app.py
