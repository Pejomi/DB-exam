import pandas as pd
import time as timer
from datetime import time
from decimal import Decimal
import main
import utils
import pyodbc


def load_and_insert(csv_path, table_name, columns, preprocess=None):
    batch_size = 1000
    batch_data = []

    # Load CSV file
    data = pd.read_csv(csv_path, encoding='utf-8', na_filter=False)

    # Optional preprocessing step
    if preprocess:
        for col, action in preprocess.items():
            if action == 'convert_to_int':
                data[col] = data[col].replace('', '0').astype(float).astype(int)
                data[col] = data[col].replace(0, None)
            elif action == 'convert_to_decimal':
                data[col] = data[col].map(utils.convert_to_decimal)
                data[col] = data[col].replace(Decimal(0), None)
            elif action == 'convert_to_time':
                data[col] = data[col].replace('', time(0, 0).strftime('%H:%M'))
                data[col] = data[col].apply(utils.to_time)
                data[col] = data[col].replace(time(0, 0).strftime('%H:%M'), None)
            elif action is None:
                data[col] = data[col].replace('', None)

    # Insert DataFrame into SQL Server
    query = f"INSERT INTO {table_name} ({', '.join(columns.keys())}) VALUES ({', '.join('?' * len(columns))})"
    for index, row in data.iterrows():
        print(f"Inserting row {index + 1} into {table_name}...")

        batch_data.append([row[col] for col in columns.values()])
        if len(batch_data) >= batch_size:
            try:
                main.cursor.executemany(query, batch_data)
                main.cnxn.commit()
                batch_data = []
            except pyodbc.Error as e:
                main.cnxn.rollback()
                print("Error occurred, transaction rolled back:", e)

    if batch_data:
        try:
            main.cursor.executemany(query, batch_data)
            main.cnxn.commit()
        except pyodbc.Error as e:
            main.cnxn.rollback()
            print("Error occurred, transaction rolled back:", e)


def insert_all_tables():
    print("Inserting lookup data into the database...")
    start = timer.time()

    # For Vehicles
    insert_vehicles_table()

    # For Severities
    insert_severities_table()

    # For AreaTypes
    insert_area_types_table()

    # For AgeBands
    insert_age_bands_table()

    # For Collisions
    insert_collisions_table()

    # For EnvironmentConditions
    insert_environment_conditions_table()

    # For Drivers
    insert_drivers_table()

    main.cursor.close()
    main.cnxn.close()

    end = timer.time()
    print(f"Lookup data inserted in {end - start} seconds.")


def insert_vehicles_table():
    load_and_insert(
        'data/table-csv/vehicles.csv',
        'Vehicles',
        {'make': 'make', 'model': 'model', 'type': 'Vehicle_Type', 'model_year': 'Model_Year'},
        preprocess={'Model_Year': 'convert_to_int', 'make': None, 'model': None, 'Vehicle_Type': None}
    )


def insert_severities_table():
    load_and_insert(
        'data/table-csv/severities.csv',
        'Severities',
        {'type': 'Accident_Severity'}
    )


def insert_area_types_table():
    load_and_insert(
        'data/table-csv/area_types.csv',
        'AreaTypes',
        {'type': 'type'}
    )


def insert_age_bands_table():
    load_and_insert(
        'data/table-csv/age_bands.csv',
        'AgeBands',
        {'band': 'Age_Band_of_Driver'}
    )


def insert_collisions_table():
    load_and_insert(
        'data/table-csv/collisions.csv',
        'Collisions',
        {'hit_object_in_carriageway': 'Hit_Object_in_Carriageway',
         'hit_object_off_carriageway': 'Hit_Object_off_Carriageway', 'vehicle_manoeuvre': 'Vehicle_Manoeuvre',
         'point_of_impact': 'X1st_Point_of_Impact'},
        preprocess={'Hit_Object_in_Carriageway': None, 'Hit_Object_off_Carriageway': None, 'Vehicle_Manoeuvre': None,
                    'X1st_Point_of_Impact': None}
    )


def insert_environment_conditions_table():
    load_and_insert(
        'data/table-csv/environment_conditions.csv',
        'EnvironmentConditions',
        {'light': 'Light_Conditions', 'weather': 'Weather_Conditions', 'road_type': 'Road_Type',
         'road_surface': 'Road_Surface_Conditions', 'speed_limit': 'Speed_limit', 'area_type_ID': 'area_type_ID'},
        preprocess={'Light_Conditions': None, 'Weather_Conditions': None, 'Road_Type': None,
                    'Road_Surface_Conditions': None, 'Speed_limit': 'convert_to_int'}
    )


def insert_drivers_table():
    load_and_insert(
        'data/table-csv/drivers.csv',
        'Drivers',
        {'age_band_ID': 'age_band_ID', 'sex': 'Sex_of_Driver', 'area_type_ID': 'area_type_ID'},
        preprocess={'Sex_of_Driver': None}
    )


def insert_accidents_table():
    load_and_insert(
        'data/table-csv/accidents.csv',
        'Accidents',
        {'vehicle_ID': 'vehicle_ID', 'driver_ID': 'driver_ID', 'severity_ID': 'severity_ID',
            'environment_conditions_ID': 'environment_conditions_ID', 'collision_ID': 'collision_ID', 'date': 'Date', 'number_of_casualties': 'Number_of_Casualties',
            'number_of_vehicles': 'Number_of_Vehicles', 'time': 'Time', 'latitude': 'Latitude', 'longitude': 'Longitude'},
        preprocess={'Number_of_Casualties': 'convert_to_int', 'Number_of_Vehicles': 'convert_to_int',
                    'Time': 'convert_to_time', 'Latitude': 'convert_to_decimal', 'Longitude': 'convert_to_decimal'}
    )