import pandas as pd


def merge_data():
    # Load CSV data
    vehicle_info = pd.read_csv('data/Vehicle_Information.csv', encoding='ISO-8859-1')
    accident_info = pd.read_csv('data/Accident_Information.csv', encoding='ISO-8859-1')

    # Drop duplicate year column
    vehicle_info = vehicle_info.drop(columns=['Year'])

    # Merge dataframes on 'Accident_Index'
    merged_data = pd.merge(accident_info, vehicle_info, on='Accident_Index')

    merged_data.to_csv('data/merged_information.csv', encoding='ISO-8859-1')
