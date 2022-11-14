FROM apache/airflow:2.4.2
USER root
RUN apt-get update \
    && apt-get install -y gcc \
    && apt-get clean
USER airflow
RUN pip install --no-cache-dir pydantic