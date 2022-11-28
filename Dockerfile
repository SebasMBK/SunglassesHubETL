FROM apache/airflow:2.4.2
USER root

RUN apt-get update \
    && apt-get install -y gcc \
    && apt-get clean \
    # This line will install the Azure CLI inside the Airflow Containers
    && curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash \
    # The next 3 lines will download de odbc driver required for connecting to Azure Synapse
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -\
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17

USER airflow
# These are the dependencies for the code. It can also be done using a requirements.txt file
# or a Piplock file
RUN pip install --no-cache-dir pydantic
RUN pip install --no-cache-dir python-dotenv
RUN pip install --no-cache-dir pyodbc
RUN pip install --no-cache-dir sqlalchemy