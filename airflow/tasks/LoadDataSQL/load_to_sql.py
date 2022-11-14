import psycopg2
from utilities import get_files_names

def load_to_sql(configuration: dict):

    """
    This function will load the data into sql.

    args:
    - configuration: These are the configuration params of the DB that will be used. This information
                     is in the form of a dictionary 
    """
    
    # This function "get_files_names" was imported from the "utilities.py" python file.
    files = get_files_names(path="/tmp/files/access/")

    conn = psycopg2.connect(**configuration)
    conn.autocommit = True
    

    for file in files:

        try:

            cursor = conn.cursor()

            # The main table
            main_table_name = "sunglasseshub_" + file.split("-")[1] + "_table"
                
            # This is the table where we will be uploading the data 
            temp_load_table_name = "temp_load_" + file.split("-")[1]

            # This is the table where we will be copying the data from the main table
            temp_copy_table_name = "temp_copy_" + file.split("-")[1]



            with open(file,'r') as csv:
                # We are ignoring the headers of the csv file, otherwise they'll be copied to de table
                next(csv)

                # Here, we are using ";" as separators. This is because there are some numbers with ",". Therefore, SQL counts them as an extra column
                cursor.copy_from(csv,f'{temp_load_table_name}',sep=';')

                print(f"Data copied to {temp_load_table_name}........")



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
                    |for copying from the directory or file itself.                                |
                    |Check the logs for more information.                                          |
                    --------------------------------------------------------------------------------
                    """)
    
    conn.close()