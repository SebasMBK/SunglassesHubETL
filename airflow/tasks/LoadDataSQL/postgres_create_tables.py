import psycopg2
from list_files import *
from config_parameters import *

def creating_tables_postgres(config_filename:str):

    """
    This function will create the tables that we need to store the sunglasseshub data that was
    extracted

    Args:
    - config_filename = The name of the ".env" file that contains the information of the SQL database.

    """

    # Database configuration parameters
    dbname = config_parameters(config_filename,"sql_databasename")
    user = config_parameters(config_filename,"sql_username")
    password = config_parameters(config_filename,"sql_password")
    host = config_parameters(config_filename,"postgres_servername")

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

    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host = host,
        port = "5432"
    )
    conn.autocommit = True


    for file in files:

        # The main table
        main_table_name = "sunglasseshub_" + file.split("-")[1] + "_table"
        
        # This is the table where we will be uploading the data 
        temp_load_table_name = "temp_load_" + file.split("-")[1]

        # This is the table where we will be copying the data from the main table
        temp_copy_table_name = "temp_copy_" + file.split("-")[1]

        # Creating a list that will be iterated by the sql statement
        table_names = [main_table_name,temp_load_table_name,temp_copy_table_name]

        for table_name in table_names:

                try:
                    cursor = conn.cursor()

                    if "temp" in table_name:

                        sql = f'''CREATE TABLE IF NOT EXISTS {table_name} ( \
                                isjunior BOOL, \
                                lenscolor VARCHAR(255), \
                                img VARCHAR(255), \
                                isfindinstore BOOL, \
                                iscustomizable BOOL, \
                                roxablelabel VARCHAR(255), \
                                brand VARCHAR(255), \
                                imghover VARCHAR(255), \
                                ispolarized BOOL, \
                                colorsnumber INT, \
                                isoutofstock BOOL, \
                                modelname VARCHAR(255), \
                                isengravable BOOL, \
                                localizedcolorlabel VARCHAR(255), \
                                listprice NUMERIC(6,2), \
                                offerprice NUMERIC(6,2),\
                                extractdate DATE \
                                );
                                '''

                    else:

                        sql = f'''CREATE TABLE IF NOT EXISTS {table_name} ( \
                                isjunior BOOL, \
                                lenscolor VARCHAR(255), \
                                img VARCHAR(255), \
                                isfindinstore BOOL, \
                                iscustomizable BOOL, \
                                roxablelabel VARCHAR(255), \
                                brand VARCHAR(255), \
                                imghover VARCHAR(255), \
                                ispolarized BOOL, \
                                colorsnumber INT, \
                                isoutofstock BOOL, \
                                modelname VARCHAR(255), \
                                isengravable BOOL, \
                                localizedcolorlabel VARCHAR(255), \
                                listprice NUMERIC(6,2), \
                                offerprice NUMERIC(6,2), \
                                extractdate DATE,
                                PRIMARY KEY (lenscolor,modelname,localizedcolorlabel) \
                                );
                                '''


                    cursor.execute(sql)
                    print(f"Table {table_name} created succesfully........")
                
                except Exception as e:
                    print("""
                    --------------------------------------------------------
                    |An error ocurred. Check the logs for more information.|
                    --------------------------------------------------------
                    """)
                
    
    conn.close()