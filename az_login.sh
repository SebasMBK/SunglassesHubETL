#!/bin/bash
echo "Please wait for the authentication code to appear"
if docker exec -ti -u airflow sunglasseshubetl_airflow-worker_1 az login ; then
    echo "Logged in successfully"
else
    docker exec -ti -u airflow sunglasseshubetl-airflow-worker-1 az login
fi

#If this script doesn't work use this command:
#docker exec -ti -u airflow name_of_the_airflow_worker_container az login
#To get the name of the airflow worker container use "docker ps"
