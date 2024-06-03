import pandas as pd
import get_db_conn
import numpy as np
import sql_queries
import clean_data
import time
import insert_from_csv
import utils

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

cnxn = get_db_conn.get_db_conn()
cursor = cnxn.cursor()


if __name__ == '__main__':
    # RUN THIS ONCE TO CREATE THE CLEANED DATA FILES
    # merge_data.merge_data()
    # data = pd.read_csv('data/merged_information.csv', encoding='ISO-8859-1')
    # clean_data.clean_data(data)

    sql_queries.create_tables_if_not_exist(cnxn)

    # Load data
    print("Loading data...")
    start_lookup = time.time()
    data = pd.read_csv('data/merged_information_clean.csv', nrows=1000, encoding='utf-8', na_filter=False)

    print("Loading existing lookup tables...")
    existing_age_bands = pd.read_sql("SELECT * FROM AgeBands", cnxn)
    existing_area_types = pd.read_sql("SELECT * FROM AreaTypes", cnxn)
    existing_collisions = pd.read_sql("SELECT * FROM Collisions", cnxn)
    existing_severities = pd.read_sql("SELECT * FROM Severities", cnxn)
    existing_vehicles = pd.read_sql("SELECT * FROM Vehicles", cnxn)

    print("Creating lookup dataframes...")

    age_bands = data[~data['Age_Band_of_Driver'].isin(existing_age_bands['band'])][
        ['Age_Band_of_Driver']].drop_duplicates()

    severities = data[~data['Accident_Severity'].isin(existing_severities['type'])][
        ['Accident_Severity']].drop_duplicates()

    collisions = utils.get_unique_collision_for_insert(existing_collisions, data)

    data['Driver_Home_Area_Type'] = data['Driver_Home_Area_Type'].replace('Urban area', 'Urban')
    area_types_array = pd.unique(pd.concat([data['Driver_Home_Area_Type'], data['Urban_or_Rural_Area']]))
    area_types = pd.DataFrame(area_types_array, columns=['type'])
    area_types = area_types[~area_types['type'].isin(existing_area_types['type'])]

    # Ensure the 'Date' column is in datetime format
    data['Date'] = pd.to_datetime(data['Date'])
    # Apply the function to calculate the model year
    data['Model_Year'] = data.apply(utils.calculate_model_year, axis=1)
    vehicles = utils.get_unique_vehicles_for_insert(existing_vehicles, data)

    age_bands.to_csv('data/table-csv/age_bands.csv', encoding='utf-8', index=False)
    severities.to_csv('data/table-csv/severities.csv', encoding='utf-8', index=False)
    area_types.to_csv('data/table-csv/area_types.csv', encoding='utf-8', index=False)
    collisions.to_csv('data/table-csv/collisions.csv', encoding='utf-8', index=False)
    vehicles.to_csv('data/table-csv/vehicles.csv', encoding='utf-8', index=False)

    insert_from_csv.insert_age_bands_table()
    insert_from_csv.insert_severities_table()
    insert_from_csv.insert_area_types_table()
    insert_from_csv.insert_collisions_table()
    insert_from_csv.insert_vehicles_table()

    end_lookup = time.time()
    print(f"Lookup dataframes created in {end_lookup - start_lookup} seconds.")

    print("Loading existing lookup tables after insert...")
    start_remaining = time.time()

    existing_age_bands = pd.read_sql("SELECT * FROM AgeBands", cnxn)
    existing_area_types = pd.read_sql("SELECT * FROM AreaTypes", cnxn)
    existing_collisions = pd.read_sql("SELECT * FROM Collisions", cnxn)
    existing_severities = pd.read_sql("SELECT * FROM Severities", cnxn)
    existing_vehicles = pd.read_sql("SELECT * FROM Vehicles", cnxn)
    existing_environment_conditions = pd.read_sql("SELECT * FROM EnvironmentConditions", cnxn)
    existing_drivers = pd.read_sql("SELECT * FROM Drivers", cnxn)
    existing_accidents = pd.read_sql("SELECT * FROM Accidents", cnxn)

    print("Creating remaining tables for insert...")
    environment_conditions = utils.get_unique_environment_conditions_for_insert(existing_environment_conditions.copy(deep=True), existing_area_types.copy(deep=True), data)
    environment_conditions.to_csv('data/table-csv/environment_conditions.csv', encoding='utf-8', index=False)
    insert_from_csv.insert_environment_conditions_table()

    drivers = utils.get_unique_drivers_for_insert(existing_drivers.copy(deep=True), existing_age_bands.copy(deep=True), existing_area_types.copy(deep=True), data)
    drivers.to_csv('data/table-csv/drivers.csv', encoding='utf-8', index=False)
    insert_from_csv.insert_drivers_table()

    existing_environment_conditions = pd.read_sql("SELECT * FROM EnvironmentConditions", cnxn)
    existing_drivers = pd.read_sql("SELECT * FROM Drivers", cnxn)

    accidents = utils.get_unique_accidents_for_insert(existing_accidents, existing_vehicles, existing_drivers, existing_severities, existing_environment_conditions, existing_collisions, existing_area_types, existing_age_bands, data)
    accidents.to_csv('data/table-csv/accidents.csv', encoding='utf-8', index=False)
    insert_from_csv.insert_accidents_table()

    end_remaining = time.time()
    print(f"Remaining tables inserted in {end_remaining - start_remaining} seconds.")

    print("Operation took a total of", end_remaining - start_lookup, "seconds.")

    cursor.close()
    cnxn.close()
