from tabnanny import check
from pydantic import ValidationError
from model_pydantic import products
from configuration_env import *
from data_cleaner import *
from list_files import *
from upload_function import *


if __name__ == "__main__":
    
    # Env Values
    configuration_filename = "configuration.env"
    access_data_directory = config_parameters(configuration_filename,"access_data_directory")
    etl_container_name = config_parameters(configuration_filename,"etl_container_name")
    raw_data_directory = config_parameters(configuration_filename,"raw_data_directory")
    storage_account_url = config_parameters(configuration_filename,"storage_account_url")

    # Cleaning process
    files = files_list(storage_url=storage_account_url, container_name=etl_container_name, data_level=raw_data_directory)

    for file in files:
        gender = file.split("-")[1]
        access_level_data = data_cleaning(storage_url=storage_account_url, container_name=etl_container_name, 
                                            data_level=raw_data_directory, filename=file)

        # This will do the validations against the pydantic model        
        try:
            validated_file = [products.parse_obj(data_) for data_ in access_level_data]
            write_to_csv = upload_to_storage(clean_data=access_level_data, storage_url=storage_account_url, 
                                                container_name=etl_container_name, data_level=access_data_directory, gender=gender)

        except ValidationError as exception:
            print(f"Sunglasses for {gender}: {exception}")
