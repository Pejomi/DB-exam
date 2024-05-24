import pandas as pd
import get_db_conn
import sql_queries
import clean_data


if __name__ == '__main__':
    data = pd.read_csv('data/merged_information.csv', encoding='ISO-8859-1')
    clean_data.clean_data(data)

    # # Get DB connection
    # cnxn = get_db_conn.get_db_conn()
    # cursor = cnxn.cursor()
    #
    # # Load data
    # data = pd.read_csv('data/merged_information_clean.csv', encoding='ISO-8859-1', nrows=100, na_filter=False)
    #
    # # Create tables if they don't exist
    # sql_queries.create_tables_if_not_exist(cnxn)
    #
    # for index, row in data.iterrows():
    #     cursor.execute("""
    #     INSERT INTO Drivers (age_band, sex, home_area_type) OUTPUT INSERTED.driver_id VALUES (?, ?, ?);""",
    #                    row['Age_Band_of_Driver'], row['Sex_of_Driver'], row['Driver_Home_Area_Type'])
    #
    #     driver_id = cursor.fetchone()[0]
    #
    #     print(row['Hit_Object_off_Carriageway'])
    #
    #     cursor.execute("""
    #             INSERT INTO Vehicles (driver_id, age, make, model, vehicle_type, hit_object_in_carriageway,
    #             hit_object_off_carriageway, vehicle_manoeuvre, point_of_impact) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
    #                    driver_id, row['Age_of_Vehicle'], row['make'], row['model'], row['Vehicle_Type'],
    #                    row['Hit_Object_in_Carriageway'], row['Hit_Object_off_Carriageway'], row['Vehicle_Manoeuvre'], row['X1st_Point_of_Impact'])
    #
    # cnxn.commit()
    # cursor.close()
    # cnxn.close()
