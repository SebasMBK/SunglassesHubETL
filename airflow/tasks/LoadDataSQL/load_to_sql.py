import psycopg2
from list_files import files_list
from config_parameters import config_parameters
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy

def load_to_sql(config_filename: dict):

    """
    This function will load the data into Potsgresql.

    args:
    - configuration: These are the configuration params of the DB that will be used. This information
                     is in the form of a dictionary 
    """

    # Database configuration parameters
    dbname = config_parameters(config_filename,"sql_databasename")
    user = config_parameters(config_filename,"sql_username")
    password = config_parameters(config_filename,"sql_password")
    host = config_parameters(config_filename,"postgres_servername")
    port = "5432"

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

    # Creating the connection to the sql server
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host = host,
        port = port
    )
    conn.autocommit = True


    for file in files:

        # The main table
        main_table_name = "sunglasseshub_" + file.split("-")[1] + "_table"
        
        # This is the temp table where we will be uploading the data initially 
        temp_load_table_name = "temp_load_" + file.split("-")[1]

        # This is the temp table where we will be copying the data from the main table
        temp_copy_table_name = "temp_copy_" + file.split("-")[1]

        try:

            # Using pandas to upload the data to the temp_load_table
            df = pd.read_csv(f"{storage_account_url}{etl_container_name}/{access_data_directory}/{file}",sep=";",index_col=False)
            engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
            df.to_sql(f"{temp_load_table_name}",con=engine,if_exists="replace",index=False,
                            dtype={"extractdate": sqlalchemy.types.DateTime()})

            print(f"Data copied to {temp_load_table_name}........")
        
            # Creating the Postgresql cursor
            cursor = conn.cursor()

            sql_temp_from_main = f"""
                                    INSERT INTO {temp_copy_table_name} \
                                    SELECT \
                                    * \
                                    FROM \
                                    {main_table_name}; \
                                """
            cursor.execute(sql_temp_from_main)
            print(f"Data copied to {temp_copy_table_name}........")


            
            sql_truncate = f'''
                            TRUNCATE {main_table_name};
                            '''
            cursor.execute(sql_truncate)
            print(f"Data truncated from {main_table_name}........")



            sql_from_temp_to_main = f"""
                                    WITH cte_table_1 AS ( \
                                    SELECT * FROM {temp_load_table_name} \
                                    UNION ALL \
                                    SELECT * FROM {temp_copy_table_name} \
                                    ), \
                                    cte_table_2 AS( \
                                    SELECT * , ROW_NUMBER() OVER(PARTITION BY lenscolor,modelname,localizedcolorlabel ORDER BY extractdate) AS order_column \
                                    FROM cte_table_1 \
                                    ), \
                                    cte_table_3 AS( \
                                    SELECT * FROM cte_table_2 \
                                    WHERE order_column = 1 \
                                    ) \
                                    \
                                    INSERT INTO {main_table_name}( \
                                    SELECT \
                                    isjunior, \
                                    lenscolor, \
                                    img, \
                                    isfindinstore, \
                                    iscustomizable, \
                                    roxablelabel, \
                                    brand, \
                                    imghover, \
                                    ispolarized, \
                                    colorsnumber, \
                                    isoutofstock, \
                                    modelname, \
                                    isengravable, \
                                    localizedcolorlabel, \
                                    listprice, \
                                    offerprice, \
                                    extractdate \
                                    FROM cte_table_3 \
                                    ) \
                                    """
            cursor.execute(sql_from_temp_to_main)
            print(f"Data ingested to {main_table_name}........")



            sql_delete_tmp_tables = f"""
                                    DROP TABLE {temp_copy_table_name}; \
                                    DROP TABLE {temp_load_table_name}; \
                                    """
            cursor.execute(sql_delete_tmp_tables)
            print(f"Temp tables deleted........")



        except Exception as e:
                    print("""
                    --------------------------------------------------------------------------------
                    |An error ocurred. Please, check that the files exists or check the permissions|
                    |for copying from the directory.                                               |
                    |Check the logs for more information.                                          |
                    --------------------------------------------------------------------------------
                    """)
                    print(e)
    
    conn.close()