from json import load
import psycopg2
from configparser import ConfigParser
import os
from data_validation import get_files_names
# Setting up the configurations
def config_parameters(filename: str, section: str):

    '''
    This function will return a dictionary with the parameters set in the ".ini" file for the
    selected database

    args:
    - filename: This is the ".ini" file that contains the parameters for the configuration of the
                database.
    - section:  This is the section of the ".ini" file that we want.


    Example of a ".ini" file:

        [postgresql]
        host=localhost
        database=postgres
        user=postgres
        password=password
        port=5432
    '''

    # Creating the parser
    parsing = ConfigParser()
    # Reading the file
    parsing.read(filename)

    # Creating the dictionary with the information of the configuration of the connection to the DB
    database_params = {}
    if parsing.has_section(section):
        parameters = parsing.items(section)
        for parameter in parameters:
            database_params[parameter[0]] = parameter[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return database_params

def creating_db(configuration: dict,db_name="scraper"):

    """
    This function will create the database in the SQL-engine that will be used for this project.

    args:
    - configuration: These are the configuration params of the DB that will be used. This information
                     is in the form of a dictionary
    - db_name: This is the name that we want to give to our database.
    """

    # Setting up the connection. In this case to a Postgresql DB.
    conn = psycopg2.connect(**configuration)
    conn.autocommit = True
    
    try:
        cursor = conn.cursor()
        sql = f'''CREATE DATABASE {db_name};'''
        cursor.execute(sql)

        conn.close()

        print("DB created succesfully........")
    except Exception as e:
        print("""
        ---------------------------------------------------------------------------------------
        |DB was already created or another error ocurred. Check the logs for more information.|
        ---------------------------------------------------------------------------------------
        """)
    
    conn.close()

def creating_tables(configuration: dict):

    """
    This function will create the tables that we need to store the sunglasseshub data that was
    extracted

    args:
    - configuration: These are the configuration params of the DB that will be used. This information
                     is in the form of a dictionary
    """

    # This function was imported from the "data_validation.py" python file.
    files = get_files_names()

    conn = psycopg2.connect(**configuration)
    conn.autocommit = True

    for file in files:
        table_name = "sunglasseshub_" + file.split("-")[1] + "_table"

        try:
            cursor = conn.cursor()
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
                    listprice money, \
                    offerprice money, \
                    PRIMARY KEY (lenscolor, modelname, localizedcolorlabel) \
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


def load_to_sql(configuration: dict):

    """
    This function will load the data into SQL.

    args:
    - configuration: These are the configuration params of the DB that will be used. This information
                     is in the form of a dictionary 
    """
    
    files = get_files_names()

    conn = psycopg2.connect(**configuration)
    conn.autocommit = True

    for file in files:
        table_name = "sunglasseshub_" + file.split("-")[1] + "_table"

        try:
            cursor = conn.cursor()
            sql_truncate = f'''
                            TRUNCATE {table_name} 
                            '''
            sql = f'''
                    COPY {table_name}(isjunior, lenscolor, img, isfindinstore, iscustomizable, roxablelabel, brand, imghover, ispolarized, colorsnumber, isoutofstock, modelname, isengravable, localizedcolorlabel, listprice, offerprice) \
                    FROM 'C:/Users/SebastianKassimMonte/OneDrive - kyndryl/Python/Web_Scrapping/sunglasseshub/SunglassesHubETL/files/access/products-{file.split("-")[1]}-access.csv' \
                    DELIMITER ',' \
                    CSV HEADER;
                    '''
            cursor.execute(sql_truncate)
            cursor.execute(sql)

            print(f"Data copied to {table_name}........")
            
        except Exception as e:
            print(f"""
            --------------------------------------------------------------------------
            |An error ocurred. Please, check that the files exists or the permissions|
            |for copying from the directory or from file itself.                     |
            |Check the logs for more information.                                    |
            --------------------------------------------------------------------------
            """)
    
    conn.close()

    

if __name__ == "__main__":
    parameters_master = config_parameters("./parameters/database.ini","postgresql_master")
    parameters_db = config_parameters("./parameters/database.ini","postgresql_scraper")
    creating_db(configuration=parameters_master,db_name="scraper")
    creating_tables(configuration=parameters_db)
    load_to_sql(configuration=parameters_db)




