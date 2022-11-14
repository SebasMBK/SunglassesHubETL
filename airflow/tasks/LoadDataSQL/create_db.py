import psycopg2

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