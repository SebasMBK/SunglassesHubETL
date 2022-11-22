import pathlib
from dotenv import dotenv_values

# Setting up the configurations
def config_parameters(filename: str, section: str):

    '''
    This function will return a dictionary with the parameters set in the ".env" file for the
    project

    args:
    - filename: This is the ".env" file that contains the parameters for the configuration of the
                database. (The name should include the ".env" extension)
    - section:  This is the section of the ".env" file that we want.


    Example of a ".env" file:

    access_data_directory = "access"
    etl_container_name = "etldatalake"
    etl_stagingarea_name = "etlstaging"
    raw_data_directory = "raw"
    storage_account_url = "https://sunglasseshubetl.blob.core.windows.net/"
    sql_password = ******
    sql_user = *****
    '''

    script_path = pathlib.Path(__file__).parent.parent.resolve()
    config_file = dotenv_values(f"{script_path}/{filename}")
    config = config_file[f"{section}"]

    return config
