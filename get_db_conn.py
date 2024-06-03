import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()



def get_db_conn():
    # Database connection parameters
    server = os.getenv("MSSQL_SERVER")
    database = 'exam_schema_v3'

    # Connect to MSSQL database
    print("Connecting to database: {}...".format(database))

    try:
        cnxn = pyodbc.connect(
            Trusted_Connection='Yes',
            Driver='{ODBC Driver 17 for SQL Server}',
            Server=f'{server}',
            Database=f'{database}',
            CHARSET='UTF-8'
        )
        print("Successfully connected to database: {}".format(database))
        return cnxn
    except pyodbc.Error:
        print("Could not connect to database: {}".format(database))
