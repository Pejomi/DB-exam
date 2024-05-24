import pandas as pd
import get_db_conn
import sql_queries
import clean_data


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
        cursor.execute("""INSERT INTO AgeBands (band) OUTPUT INSERTED.age_band_id VALUES (?);""",
                       row['Age_Band_of_Driver'])

        age_band_id = cursor.fetchone()[0]

        cursor.execute("""INSERT INTO AreaTypes (type) OUTPUT INSERTED.area_type_id VALUES (?);""",
                       row['Driver_Home_Area_Type'])

        area_type_id = cursor.fetchone()[0]

        # cursor.execute("""INSERT INTO Collisions

        
        cursor.execute("""
        INSERT INTO Drivers (age_band, sex, home_area_type) OUTPUT INSERTED.driver_id VALUES (?, ?, ?);""",
                       row['Age_Band_of_Driver'], row['Sex_of_Driver'], row['Driver_Home_Area_Type'])


    cnxn.commit()
    cursor.close()
    cnxn.close()
