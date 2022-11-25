import pyodbc
from list_files import *
from config_parameters import *

def load_to_synapse(config_filename:str):

    """
    This function will upload data to the created the tables.

    Args:
    - config_filename = The name of the ".env" file that contains the information of the SQL database.

    """

    # Database configuration parameters
    sql_pool_dbname = config_parameters(config_filename,"sql_pool_dbname")
    user = config_parameters(config_filename,"sql_username")
    password = config_parameters(config_filename,"sql_password")
    host = config_parameters(config_filename,'"sql"')

    # Storage account configuration parameters
    storage_account_url = config_parameters(config_filename,"storage_account_url")
    etl_container_name = config_parameters(config_filename,"etl_container_name")
    access_data_directory = config_parameters(config_filename,"access_data_directory")

    # List of the access level files' names that are stored inside our storage account
    files = files_list(
        storage_url=storage_account_url,
        container_name=etl_container_name,
        data_level=access_data_directory
        )

    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+host+';DATABASE='+sql_pool_dbname+';PORT=1433;UID='+user+';PWD='+ password)
    conn.autocommit = True


    for file in files:

        # The main table
        main_table_name = "sunglasseshub_" + file.split("-")[1] + "_table"

        try:
            cursor = conn.cursor()

            sql_truncate = f''' 
                         TRUNCATE TABLE {main_table_name};
                    '''
            
            cursor.execute(sql_truncate)
            print(F"{main_table_name} table truncated........")

            sql_upload = f''' COPY INTO {main_table_name} \
                       FROM '{storage_account_url}{etl_container_name}/{access_data_directory}/{file}' \
                       WITH ( \
                       FILE_TYPE = 'CSV', \
                       FIELDTERMINATOR=';', \
                       FIRSTROW = 2 \
                       ) 
                    '''

            cursor.execute(sql_upload)
            print(f"Data uploaded succesfully to {main_table_name}........")
                
        except Exception as e:
            print("""
                --------------------------------------------------------
                |An error ocurred. Check the logs for more information.|
                --------------------------------------------------------
                """)
            print(e)                
    
    conn.close()