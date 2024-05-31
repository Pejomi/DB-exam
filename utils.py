from decimal import Decimal
from datetime import datetime, time

import pandas as pd


# Function to calculate the model year considering the month of the accident
def calculate_model_year(row):
    # Check if either 'Age_of_Vehicle' or 'Date' is NaN
    if row['Age_of_Vehicle'] == '' or row['Date'] == '':
        return None

    accident_year = row['Date'].year
    accident_month = row['Date'].month
    age_of_vehicle = row['Age_of_Vehicle']

    # Calculate preliminary model year
    preliminary_model_year = accident_year - int(age_of_vehicle)

    # Adjust for early-year accidents, assuming new models are bought up to 3 months before the end of the year
    if accident_month <= 3:
        return preliminary_model_year - 1
    return preliminary_model_year


def get_unique_collision_for_insert(existing_collisions, data):
    existing_collisions.fillna('unknown', inplace=True)
    new_collisions = pd.DataFrame(data[['Hit_Object_in_Carriageway', 'Hit_Object_off_Carriageway', 'Vehicle_Manoeuvre', 'X1st_Point_of_Impact']])
    new_collisions.replace('', 'unknown', inplace=True)

    existing_collisions.rename(columns={
        'hit_object_in_carriageway': 'Hit_Object_in_Carriageway',
        'hit_object_off_carriageway': 'Hit_Object_off_Carriageway',
        'vehicle_manoeuvre': 'Vehicle_Manoeuvre',
        'point_of_impact': 'X1st_Point_of_Impact'
    }, inplace=True)

    # Merge data with existing_collisions on the specified columns
    merged = pd.merge(new_collisions, existing_collisions,
                      on=['Hit_Object_in_Carriageway', 'Hit_Object_off_Carriageway', 'Vehicle_Manoeuvre', 'X1st_Point_of_Impact'],
                      how='left', indicator=True)

    # Filter out rows that found a match
    collisions = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

    # Optionally, if you need to keep only the specified columns and remove duplicates
    collisions = collisions.drop_duplicates()
    collisions.replace('unknown', None, inplace=True)

    return collisions


def get_unique_vehicles_for_insert(existing_vehicles, data):
    existing_vehicles[['make', 'model', 'type']] = existing_vehicles[['make', 'model', 'type']].fillna('unknown')
    existing_vehicles['model_year'] = existing_vehicles['model_year'].fillna(0).astype(int)

    new_vehicles = pd.DataFrame(data[['make', 'model', 'Vehicle_Type', 'Model_Year']])
    new_vehicles[['make', 'model', 'Vehicle_Type']] = new_vehicles[['make', 'model', 'Vehicle_Type']].replace('', 'unknown')
    new_vehicles['Model_Year'] = new_vehicles['Model_Year'].fillna(0).astype(float).astype(int)
    new_vehicles['Model_Year'] = new_vehicles['Model_Year'].replace('', 0).astype(float).astype(int)

    existing_vehicles.rename(columns={
        'make': 'make',
        'model': 'model',
        'type': 'Vehicle_Type',
        'model_year': 'Model_Year'
    }, inplace=True)

    # Merge data with existing_vehicles on the specified columns
    merged = pd.merge(new_vehicles, existing_vehicles,
                      on=['make', 'model', 'Vehicle_Type', 'Model_Year'],
                      how='left', indicator=True)

    # Filter out rows that found a match
    vehicles = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

    # Optionally, if you need to keep only the specified columns and remove duplicates
    vehicles = vehicles.drop_duplicates()
    vehicles.replace('unknown', None, inplace=True)
    vehicles['Model_Year'] = vehicles['Model_Year'].replace(0, None)

    return vehicles


def get_unique_environment_conditions_for_insert(existing_environment_conditions, existing_area_types, data):
    existing_environment_conditions = existing_environment_conditions.drop(columns=['environment_conditions_ID'])
    existing_environment_conditions[['light', 'weather', 'road_type', 'road_surface']].fillna('unknown', inplace=True)
    existing_environment_conditions['speed_limit'] = existing_environment_conditions['speed_limit'].fillna(0).astype(int)

    new_environment_conditions = pd.DataFrame(data[['Light_Conditions', 'Weather_Conditions', 'Road_Type', 'Road_Surface_Conditions', 'Urban_or_Rural_Area', 'Speed_limit']])
    new_environment_conditions[['Light_Conditions', 'Weather_Conditions', 'Road_Type', 'Road_Surface_Conditions']].replace('', 'unknown', inplace=True)
    new_environment_conditions['Speed_limit'] = new_environment_conditions['Speed_limit'].replace('', 0).astype(float).astype(int)
    new_environment_conditions['Speed_limit'] = new_environment_conditions['Speed_limit'].fillna(0).astype(float).astype(int)

    existing_area_types.rename(columns={'type': 'Urban_or_Rural_Area'}, inplace=True)
    matching_area_type = pd.merge(new_environment_conditions, existing_area_types, on='Urban_or_Rural_Area', how='inner')
    area_type_id = matching_area_type['area_type_ID']
    new_environment_conditions['area_type_ID'] = area_type_id

    existing_environment_conditions.rename(columns={
        'light': 'Light_Conditions',
        'weather': 'Weather_Conditions',
        'road_type': 'Road_Type',
        'road_surface': 'Road_Surface_Conditions',
        'speed_limit': 'Speed_limit'
    }, inplace=True)

    merged = pd.merge(new_environment_conditions, existing_environment_conditions,
                        on=['Light_Conditions', 'Weather_Conditions', 'Road_Type', 'Road_Surface_Conditions', 'Speed_limit', 'area_type_ID'],
                        how='left', indicator=True)

    # Filter out rows that found a match
    environment_conditions = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

    # Optionally, if you need to keep only the specified columns and remove duplicates
    environment_conditions = environment_conditions.drop_duplicates()
    environment_conditions.replace('unknown', None, inplace=True)
    environment_conditions['Speed_limit'] = environment_conditions['Speed_limit'].replace(0, None)

    return environment_conditions


def get_unique_drivers_for_insert(existing_drivers, existing_age_bands, existing_area_types, data):
    existing_drivers = existing_drivers.drop(columns=['driver_ID'])
    existing_drivers['sex'].fillna('unknown', inplace=True)

    new_drivers = pd.DataFrame(data[['Sex_of_Driver', 'Age_Band_of_Driver', 'Driver_Home_Area_Type']])
    new_drivers.replace('', 'unknown', inplace=True)

    existing_age_bands.rename(columns={'band': 'Age_Band_of_Driver'}, inplace=True)
    matching_age_band = pd.merge(new_drivers, existing_age_bands, on='Age_Band_of_Driver', how='inner')
    age_band_id = matching_age_band['age_band_ID']
    new_drivers['age_band_ID'] = age_band_id

    existing_area_types.rename(columns={'type': 'Driver_Home_Area_Type'}, inplace=True)
    matching_area_type = pd.merge(new_drivers, existing_area_types, on='Driver_Home_Area_Type', how='inner')
    area_type_id = matching_area_type['area_type_ID']
    new_drivers['area_type_ID'] = area_type_id

    existing_drivers.rename(columns={
        'sex': 'Sex_of_Driver'
    }, inplace=True)

    merged = pd.merge(new_drivers, existing_drivers,
                      on=['Sex_of_Driver', 'age_band_ID', 'area_type_ID'],
                        how='left', indicator=True)

    # Filter out rows that found a match
    drivers = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

    # Optionally, if you need to keep only the specified columns and remove duplicates
    drivers = drivers.drop_duplicates()
    drivers.replace('unknown', None, inplace=True)

    return drivers


def get_unique_accidents_for_insert(existing_accidents, existing_vehicles, existing_drivers, existing_severities, existing_environment_conditions, existing_collisions, existing_area_types, existing_age_bands, data):
    existing_accidents = existing_accidents.drop(columns=['accident_ID'])
    existing_accidents['time'] = existing_accidents['time'].fillna(time(0, 0, 0)).apply(to_time)

    existing_accidents[['number_of_casualties', 'number_of_vehicles']].fillna(0, inplace=True)
    existing_accidents[['latitude', 'longitude']] = existing_accidents[['latitude', 'longitude']].map(convert_to_decimal)
    existing_accidents['date'] = pd.to_datetime(existing_accidents['date'])

    existing_vehicles[['make', 'model', 'type']] = existing_vehicles[['make', 'model', 'type']].fillna('unknown')
    existing_vehicles['model_year'] = existing_vehicles['model_year'].fillna(0).astype(int)

    existing_drivers['sex'].fillna('unknown', inplace=True)

    existing_environment_conditions[['light', 'weather', 'road_type', 'road_surface']].fillna('unknown', inplace=True)
    existing_environment_conditions['speed_limit'] = existing_environment_conditions['speed_limit'].fillna(0).astype(int)

    existing_collisions.fillna('unknown', inplace=True)

    ##############################

    new_accidents = data.copy()

    new_accidents['Time'] = new_accidents['Time'].replace('', time(0, 0, 0)).apply(to_time)

    new_accidents[['Number_of_Casualties', 'Number_of_Vehicles']] = new_accidents[['Number_of_Casualties', 'Number_of_Vehicles']].fillna(0).astype(float).astype(int)
    new_accidents[['Latitude', 'Longitude']] = new_accidents[['Latitude', 'Longitude']].map(convert_to_decimal)

    new_accidents[['make', 'model', 'Vehicle_Type']] = new_accidents[['make', 'model', 'Vehicle_Type']].replace('', 'unknown')

    # Ensure the 'Date' column is in datetime format
    new_accidents['Date'] = pd.to_datetime(new_accidents['Date'])
    # Apply the function to calculate the model year
    new_accidents['Model_Year'] = new_accidents.apply(calculate_model_year, axis=1)
    new_accidents['Model_Year'] = new_accidents['Model_Year'].fillna(0).astype(float).astype(int)
    new_accidents['Model_Year'] = new_accidents['Model_Year'].replace('', 0).astype(float).astype(int)

    new_accidents[['Sex_of_Driver', 'Age_Band_of_Driver', 'Driver_Home_Area_Type']].replace('', 'unknown', inplace=True)

    new_accidents[['Light_Conditions', 'Weather_Conditions', 'Road_Type', 'Road_Surface_Conditions']].replace('', 'unknown', inplace=True)
    new_accidents['Speed_limit'] = new_accidents['Speed_limit'].replace('', 0).astype(float).astype(int)
    new_accidents['Speed_limit'] = new_accidents['Speed_limit'].fillna(0).astype(float).astype(int)

    new_accidents[['Hit_Object_in_Carriageway', 'Hit_Object_off_Carriageway', 'Vehicle_Manoeuvre', 'X1st_Point_of_Impact']] = new_accidents[['Hit_Object_in_Carriageway', 'Hit_Object_off_Carriageway', 'Vehicle_Manoeuvre', 'X1st_Point_of_Impact']].replace('', 'unknown')

    ##############################

    existing_area_types.rename(columns={'type': 'Urban_or_Rural_Area'}, inplace=True)
    matching_area_type = pd.merge(new_accidents, existing_area_types, on='Urban_or_Rural_Area', how='inner')
    area_type_id = matching_area_type['area_type_ID'].astype(float).astype(int)
    new_accidents['environment_area_type_ID'] = area_type_id

    existing_area_types.rename(columns={'Urban_or_Rural_Area': 'Driver_Home_Area_Type'}, inplace=True)
    matching_area_type = pd.merge(new_accidents, existing_area_types, on='Driver_Home_Area_Type', how='inner')
    area_type_id = matching_area_type['area_type_ID'].astype(float).astype(int)
    new_accidents['home_area_type_ID'] = area_type_id

    existing_age_bands.rename(columns={'band': 'Age_Band_of_Driver'}, inplace=True)
    matching_age_band = pd.merge(new_accidents, existing_age_bands, on='Age_Band_of_Driver', how='inner')
    age_band_id = matching_age_band['age_band_ID'].astype(float).astype(int)
    new_accidents['age_band_ID'] = age_band_id

    ##############################

    existing_environment_conditions.rename(columns={
        'light': 'Light_Conditions',
        'weather': 'Weather_Conditions',
        'road_type': 'Road_Type',
        'road_surface': 'Road_Surface_Conditions',
        'speed_limit': 'Speed_limit',
        'area_type_ID': 'environment_area_type_ID'
    }, inplace=True)

    merged = pd.merge(new_accidents, existing_environment_conditions,
                        on=['Light_Conditions', 'Weather_Conditions', 'Road_Type', 'Road_Surface_Conditions', 'Speed_limit', 'environment_area_type_ID'],
                        how='left', indicator=True)

    # Keep only the rows that found a match
    environtment_conditions_ids = merged[merged['_merge'] == 'both'].drop(columns=['_merge'])['environment_conditions_ID'].astype(float).astype(int)

    new_accidents['environment_conditions_ID'] = environtment_conditions_ids

    ##############################

    existing_drivers.rename(columns={
        'sex': 'Sex_of_Driver',
        'area_type_ID': 'home_area_type_ID'
    }, inplace=True)

    merged = pd.merge(new_accidents, existing_drivers,
                      on=['Sex_of_Driver', 'age_band_ID', 'home_area_type_ID'],
                        how='left', indicator=True)

    # Keep only the rows that found a match
    driver_ids = merged[merged['_merge'] == 'both'].drop(columns=['_merge'])['driver_ID'].astype(float).astype(int)

    new_accidents['driver_ID'] = driver_ids

    ##############################

    existing_vehicles.rename(columns={
        'make': 'make',
        'model': 'model',
        'type': 'Vehicle_Type',
        'model_year': 'Model_Year'
    }, inplace=True)

    # Merge data with existing_vehicles on the specified columns
    merged = pd.merge(new_accidents, existing_vehicles,
                      on=['make', 'model', 'Vehicle_Type', 'Model_Year'],
                      how='left', indicator=True)

    # Keep only the rows that found a match
    vehicle_ids = merged[merged['_merge'] == 'both'].drop(columns=['_merge'])['vehicle_ID'].astype(float).astype(int)

    new_accidents['vehicle_ID'] = vehicle_ids

    ##############################

    existing_collisions.rename(columns={
        'hit_object_in_carriageway': 'Hit_Object_in_Carriageway',
        'hit_object_off_carriageway': 'Hit_Object_off_Carriageway',
        'vehicle_manoeuvre': 'Vehicle_Manoeuvre',
        'point_of_impact': 'X1st_Point_of_Impact'
    }, inplace=True)

    # Merge data with existing_collisions on the specified columns
    merged = pd.merge(new_accidents, existing_collisions,
                      on=['Hit_Object_in_Carriageway', 'Hit_Object_off_Carriageway', 'Vehicle_Manoeuvre', 'X1st_Point_of_Impact'],
                      how='left', indicator=True)

    # Keep only the rows that found a match
    collision_ids = merged[merged['_merge'] == 'both'].drop(columns=['_merge'])['collision_ID'].astype(float).astype(int)

    new_accidents['collision_ID'] = collision_ids

    ##############################

    existing_severities.rename(columns={'type': 'Accident_Severity'}, inplace=True)
    matching_severity = pd.merge(new_accidents, existing_severities, on='Accident_Severity', how='inner')
    severity_id = matching_severity['severity_ID'].astype(float).astype(int)
    new_accidents['severity_ID'] = severity_id

    ##############################

    existing_accidents.rename(columns={
        'vehicle_ID': 'vehicle_ID',
        'driver_ID': 'driver_ID',
        'severity_ID': 'severity_ID',
        'environment_conditions_ID': 'environment_conditions_ID',
        'collision_ID': 'collision_ID',
        'date': 'Date',
        'number_of_casualties': 'Number_of_Casualties',
        'number_of_vehicles': 'Number_of_Vehicles',
        'time': 'Time',
        'latitude': 'Latitude',
        'longitude': 'Longitude'
    }, inplace=True)

    merged = pd.merge(new_accidents, existing_accidents,
                        on=['vehicle_ID', 'driver_ID', 'severity_ID', 'environment_conditions_ID', 'collision_ID', 'Date', 'Number_of_Casualties', 'Number_of_Vehicles', 'Time', 'Latitude', 'Longitude'],
                        how='left', indicator=True)

    # Filter out rows that found a match
    accidents = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

    # Optionally, if you need to keep only the specified columns and remove duplicates
    accidents = accidents.drop_duplicates()

    accidents.replace('unknown', None, inplace=True)
    accidents.replace(0, None, inplace=True)
    accidents.replace(time(0, 0).strftime('%H:%M'), None, inplace=True)

    return accidents[['vehicle_ID', 'driver_ID', 'severity_ID', 'environment_conditions_ID', 'collision_ID', 'Date', 'Number_of_Casualties', 'Number_of_Vehicles', 'Time', 'Latitude', 'Longitude']]


def convert_to_decimal(x):
    try:
        return Decimal(x).quantize(Decimal('.000001'))
    except:
        return Decimal(0)


def to_time(t):
    try:
        return datetime.strptime(str(t), '%H:%M').time()
    except:
        return datetime.strptime(str(t), '%H:%M:%S').time()
