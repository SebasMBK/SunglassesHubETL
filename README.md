# SunglassesHubETL
*This project is for demonstrating knowledge of Data Engineering tools and concepts and also learning in the process*

This Pipeline extracts data from [Sunglasseshut](https://www.sunglasshut.com) web page that will be sinked into a Power BI dashboard.

The tools that were used for this project are the following:
- [Azure](https://azure.microsoft.com/)  for hosting the infraestructure.
- [Terraform](https://www.terraform.io/) as IaaC for infra provisioning.
- [Airflow](https://airflow.apache.org/) for orchestration.
- [Docker](https://www.docker.com/) for containerizing the pipeline.
- [Insomnia](https://insomnia.rest/) for obtaining the code that sends request to the Web page API.
- [Power BI](https://powerbi.microsoft.com/) for data visualization.
- [Python](https://www.python.org/) as the main programming language.

## Project's Architecture
![Projects Architecture](https://github.com/SebasMBK/SunglassesHubETL/blob/a556bf21b3f929e4261d68ae840bd754b962fc63/images/azure_etl.png)

1. Scraping the data using insomnia and python.
2. The extracted data is converted into a Dataframe that is uploaded to Azure Storage account using the Azure Identity and Azure Blob Storage client libraries.
3. The data is cleaned and the data types are validated using pydantic's data classes.
4. Finally, we deliver the data to Azure Synapse (Datawarehouse) and Azure Database for PostgreSQL - Flexible Server.
5. Users can now analyze the data using Power BI or whatever visualization tool they prefer.

## Dashboard
![Project Dashboard Expensive](https://github.com/SebasMBK/SunglassesHubETL/blob/main/images/Sunglasseshutetl_dashboard.png)
![Project Dashboard Cheap](https://github.com/SebasMBK/SunglassesHubETL/blob/main/images/Sunglasseshutetl_dashboard_cheapest.png)

## Project's requirements
It is necessary to install and configure the following tools for the correct functioning of the pipeline:
1. [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) for account configuring and terraform provisioning.
2. [Terraform](https://www.terraform.io/) to provision the infraestructure.
3. [Docker](https://www.docker.com/) for running airflow and containerizing the pipeline.
4. (Optional) Linux OS to use the "Makefile" make commands.

## Start Pipeline
The following commands can be used to initialize the pipeline, but they will only work on Linux OS.
1. `make init-terraform`: Initialize the Terraform backend inside the ./terraform directory. You'll be asked to insert first a password and then a user. These same credentials will be used for both Azure Synapse and PostgreSQL.
2. `make environment`: Provision the Azure infraestructure using Terraform.
3. `make terraform-config`: Outputs the configuration of the infra created with Terraform into a file called "configuration.env" inside ./airflow/tasks. This file includes FQDN, database names, etc.
4. `make start-run`: Creates and starts the airflow containers.
5. `make az-login`: Login to Azure from within the container. Necessary for all the Airflow tasks. This will prompt you with an authentication url and code. Follow the instructions closely.

Now you can login into Airflow through http://localhost:8080/ and trigger the pipeline manually or wait for the next scheduled run. The user and password should be "airflow". You can change this from the docker-compose file.
