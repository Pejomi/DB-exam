import pandas as pd


def clean_data(data):
    cleaned_data = data[[
        "Accident_Index",
        "Accident_Severity",
        "Date",
        "Latitude",
        "Longitude",
        "Light_Conditions",
        "Number_of_Casualties",
        "Number_of_Vehicles",
        "Speed_limit",
        "Time",
        "Weather_Conditions",
        "Road_Type",
        "Road_Surface_Conditions",
        "Urban_or_Rural_Area",
        "Age_Band_of_Driver",
        "Age_of_Vehicle",
        "make",
        "model",
        "Sex_of_Driver",
        "Vehicle_Type",
        "Hit_Object_in_Carriageway",
        "Hit_Object_off_Carriageway",
        "Vehicle_Manoeuvre",
        "Driver_Home_Area_Type",
        "X1st_Point_of_Impact"
    ]]

    int_columns = ['Age_of_Vehicle', 'Number_of_Vehicles', 'Number_of_Casualties', 'Speed_limit']

    # Fill nan values with -1, and convert the columns to int
    cleaned_data[['Age_of_Vehicle', 'Number_of_Vehicles', 'Number_of_Casualties', 'Speed_limit']] = (
        cleaned_data[['Age_of_Vehicle', 'Number_of_Vehicles', 'Number_of_Casualties', 'Speed_limit']].astype('Int64'))

    # Get all other columns as string columns, excluding the specified non-string columns
    string_columns = [col for col in cleaned_data.columns if col not in int_columns]

    # Replace NaN and empty strings
    cleaned_data[string_columns] = cleaned_data[string_columns].replace({'Data missing or out of range': 'No data', '': 'No data'})

    cleaned_data.to_csv('data/merged_information_clean.csv', encoding='utf-8')
