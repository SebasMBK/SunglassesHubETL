import pyodbc
from list_files import *
from config_parameters import *

def creating_tables_synapse(config_filename:str):

    """
    This function will create the tables that we need to store the sunglasseshub data that was
    extracted

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

            sql = f'''IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{main_table_name}' and xtype='U') \
                    CREATE TABLE {main_table_name} ( \
                    isjunior VARCHAR(6), \
                    lenscolor VARCHAR(255) NOT NULL, \
                    img VARCHAR(255), \
                    isfindinstore VARCHAR(6), \
                    iscustomizable VARCHAR(6), \
                    roxablelabel VARCHAR(255), \
                    brand VARCHAR(255), \
                    imghover VARCHAR(255), \
                    ispolarized VARCHAR(6), \
                    colorsnumber INT, \
                    isoutofstock VARCHAR(6), \
                    modelname VARCHAR(255) NOT NULL, \
                    isengravable VARCHAR(6), \
                    localizedcolorlabel VARCHAR(255) NOT NULL, \
                    listprice NUMERIC(6,2), \
                    offerprice NUMERIC(6,2), \
                    extractdate DATE
                    )
                    WITH (DISTRIBUTION = REPLICATE);
                    '''

            cursor.execute(sql)
            print(f"Table {main_table_name} created succesfully........")
                
        except Exception as e:
            print("""
                --------------------------------------------------------
                |An error ocurred. Check the logs for more information.|
                --------------------------------------------------------
                """)
            print(e)                
    
    conn.close()