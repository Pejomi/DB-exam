import pandas as pd
import get_db_conn
import sql_queries
import clean_data


def check_null(value):
    if value == 'No data' or value == '':
        return None
    else:
        return value


if __name__ == '__main__':
    # data = pd.read_csv('data/merged_information.csv', encoding='ISO-8859-1')
    # clean_data.clean_data(data)

    # Get DB connection
    cnxn = get_db_conn.get_db_conn()
    cursor = cnxn.cursor()

    # Load data
    data = pd.read_csv('data/merged_information_clean.csv', encoding='utf-8', nrows=100, na_filter=False)

    # Create tables if they don't exist
    sql_queries.create_tables_if_not_exist(cnxn)

    for index, row in data.iterrows():
        cursor.execute("""
                INSERT INTO Drivers (age_band, sex, home_area_type) OUTPUT INSERTED.driver_id VALUES (?, ?, ?);""",
                       check_null(row['Age_Band_of_Driver']), check_null(row['Sex_of_Driver']), check_null(row['Driver_Home_Area_Type']))

        driver_id = cursor.fetchone()[0]

        cursor.execute("""
                INSERT INTO Vehicles (driver_id, age, make, model, vehicle_type, hit_object_in_carriageway,
                hit_object_off_carriageway, vehicle_manoeuvre, point_of_impact) OUTPUT INSERTED.vehicle_id VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                       driver_id, check_null(row['Age_of_Vehicle']), check_null(row['make']), check_null(row['model']),
                       check_null(row['Vehicle_Type']), check_null(row['Hit_Object_in_Carriageway']),
                       check_null(row['Hit_Object_off_Carriageway']), check_null(row['Vehicle_Manoeuvre']),
                       check_null(row['X1st_Point_of_Impact']))

        vehicle_id = cursor.fetchone()[0]

        cursor.execute("""
                INSERT INTO Accidents (vehicles_id, severity, date, latitude, longitude, light_conditions,
                number_of_casualties, number_of_vehicles, speed_limit, time, weather_conditions, road_type, 
                road_surface_conditions, urban_or_rural_area) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                       vehicle_id, check_null(row['Accident_Severity']), check_null(row['Date']),
                       check_null(row['Latitude']), check_null(row['Longitude']), check_null(row['Light_Conditions']),
                       check_null(row['Number_of_Casualties']), check_null(row['Number_of_Vehicles']),
                       check_null(row['Speed_limit']), check_null(row['Time']), check_null(row['Weather_Conditions']),
                       check_null(row['Road_Type']), check_null(row['Road_Surface_Conditions']), check_null(row['Urban_or_Rural_Area']))

    cnxn.commit()
    cursor.close()
    cnxn.close()
