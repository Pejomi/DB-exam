import pyodbc


def get_db_conn():
    # Database connection parameters
    server = '.'
    database = 'exam_schema_v1'

    # Connect to MSSQL database
    print("Connecting to database: {}...".format(database))

    try:
        cnxn = pyodbc.connect(
            Trusted_Connection='Yes',
            Driver='{ODBC Driver 17 for SQL Server}',
            Server=f'{server}',
            Database=f'{database}'
        )
        print("Successfully connected to database: {}".format(database))
        return cnxn
    except pyodbc.Error:
        print("Could not connect to database: {}".format(database))
