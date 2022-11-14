import psycopg2
from configparser import ConfigParser
from utilities import get_files_names
from config_parameters import config_parameters
from create_db import creating_db
from sql_create_tables import creating_tables
from load_to_sql import load_to_sql
import pathlib


if __name__ == "__main__":
    database_conf_path = str(pathlib.Path(__file__).parent.resolve()) + "/parameters/database.ini"
    parameters_master = config_parameters(database_conf_path,"postgresql_master")
    parameters_db = config_parameters(database_conf_path,"postgresql_scraper")
    creating_db(configuration=parameters_master,db_name=parameters_db['database'])
    creating_tables(configuration=parameters_db)
    load_to_sql(configuration=parameters_db)
