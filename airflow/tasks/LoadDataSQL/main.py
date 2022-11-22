from sql_create_tables import creating_tables
from load_to_sql import load_to_sql


if __name__ == "__main__":
    config_filename = "configuration.env"
    creating_tables(config_filename=config_filename)
    load_to_sql(config_filename=config_filename)
