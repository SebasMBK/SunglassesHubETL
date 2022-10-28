FROM apache/airflow:2.3.0-python3.9

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get autoremove -yqq --purge \
    && apt-get -y install libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# We already have a requirements.txt file, so we are going to directly COPY that to the docker container and install the dependencies from there.
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt