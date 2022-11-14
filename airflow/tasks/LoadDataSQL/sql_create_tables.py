import psycopg2
from utilities import get_files_names

def creating_tables(configuration: dict):

    """
    This function will create the tables that we need to store the sunglasseshub data that was
    extracted

    args:
    - configuration: These are the configuration params of the DB that will be used. This information
                     is in the form of a dictionary
    """

    # This function "get_files_names" was imported from the "utilities.py" python file.
    files = get_files_names(path="/tmp/files/access/")

    conn = psycopg2.connect(**configuration)
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
                                listprice MONEY, \
                                offerprice MONEY,\
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
                                listprice MONEY, \
                                offerprice MONEY, \
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