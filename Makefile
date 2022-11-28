help: 
		@echo " build:     			Builds the docker images from the docker-compose file"
		@echo " start:     			Starts the containers created from the docker-compose file"
		@echo " start-run:			Creates and starts containers for airflow"
		@echo " stop-airflow:			Stops containers created from the docker-compose file"
		@echo " init-terraform:		Initializes terraform configuration"
		@echo " environment:			Builds the Azure Cloud infra using terraform"
		@echo " terraform-config:		Creates the configuration.env file from terraform output.tf file"
		@echo " remove-airflow:		Removes containers created by build/start-run command"

init-terraform:
		cd ./terraform && terraform init
environment:
		cd ./terraform && terraform apply
terraform-config:
		cd ./terraform && terraform output > ../airflow/tasks/configuration.env
build:
		sudo docker-compose build
start:
		sudo docker-compose start
start-run:
		sudo docker-compose up -d
stop-airflow:
		sudo docker-compose stop
remove-airflow:
		sudo docker-compose down
