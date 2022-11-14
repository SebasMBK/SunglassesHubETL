from configparser import ConfigParser
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
