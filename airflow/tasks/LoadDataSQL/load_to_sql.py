import psycopg2
from configparser import ConfigParser
from utilities import get_files_names
import pathlib

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

    # This function "get_files_names" was imported from the "utilities.py" python file.
    files = get_files_names(path="/tmp/files/access/")

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
                    listprice MONEY, \
                    offerprice MONEY, \
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
    
    # This function "get_files_names" was imported from the "utilities.py" python file.
    files = get_files_names(path="/tmp/files/access/")

    conn = psycopg2.connect(**configuration)
    conn.autocommit = True

    try:

        cursor = conn.cursor()

        for file in files:
            table_name = "sunglasseshub_" + file.split("-")[1] + "_table"

            sql_truncate = f'''
                            TRUNCATE {table_name} 
                            '''
            cursor.execute(sql_truncate)

            with open(file,'r') as csv:
                # We are ignoring the headers of the csv file, otherwise they'll be copied to de table
                next(csv)

                # Here, we are using ";" as separators. This is because there are some numbers with ",". Therefore, SQL counts them as an extra column
                cursor.copy_from(csv,f'{table_name}',sep=';')



            print(f"Data copied to {table_name}........")

    except Exception as e:
                print("""
                --------------------------------------------------------------------------------
                |An error ocurred. Please, check that the files exists or check the permissions|
                |for copying from the directory or file itself.                                |
                |Check the logs for more information.                                          |
                --------------------------------------------------------------------------------
                """)
    
    conn.close()

    

if __name__ == "__main__":
    database_conf_path = str(pathlib.Path(__file__).parent.resolve()) + "/parameters/database.ini"
    parameters_master = config_parameters(database_conf_path,"postgresql_master")
    parameters_db = config_parameters(database_conf_path,"postgresql_scraper")
    creating_db(configuration=parameters_master,db_name=parameters_db['database'])
    creating_tables(configuration=parameters_db)
    load_to_sql(configuration=parameters_db)