import pyodbc

sql_files = [
    'sql-files/create_accidents_table.sql',
    'sql-files/create_drivers_table.sql',
    'sql-files/create_vehicles_table.sql'
]


def execute_sql_from_file(filepath, cnxn):
    try:
        with open(filepath, 'r') as file:  # Open the file to read the SQL command
            sql_query = file.read()  # Read the entire SQL file into a string
        cursor = cnxn.cursor()  # Create a cursor from the connection
        cursor.execute(sql_query)  # Execute the SQL command
        cnxn.commit()  # Commit the transaction
    except Exception as e:
        print(f"An error occurred while executing SQL from {filepath}: {e}")


def create_tables_if_not_exist(cnxn):
    print("Creating tables if they don't exist...")

    # Execute each SQL file
    for file_path in sql_files:
        execute_sql_from_file(file_path, cnxn)
