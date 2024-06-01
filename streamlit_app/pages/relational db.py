import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
st.set_page_config(page_title="Relational DB", page_icon="../img/logo.png")

tab1, tab2, tab3 = st.tabs(["Search", "Analyze", "🔥Adminstrator"])

def search():
    # make a query to the database with transaction

    accident_severity = "severity IN (?) AND number_of_casualties BETWEEN ? AND ? AND timestamp BETWEEN ? AND ?"
    driver = "sex IN (?) AND home_area_type = ? AND age_bands IN (?)"
    vehicle = "vehicle_type IN (?) AND vehicle_make IN (?)"
    environment_conditions = "weather IN (?) AND road_type IN (?) AND speed_limit IN (?) AND light IN (?) AND road_surface IN (?) AND area_type IN (?)"

    query = "SELECT * FROM accidents WHERE " + accident_severity + " AND " + driver + " AND " + vehicle + " AND " + environment_conditions + " LIMIT ?, ?"
    # query = "SELECT * FROM accidents WHERE severity IN (?) AND number_of_casualties BETWEEN ? AND ? AND timestamp BETWEEN ? AND ? AND sex IN (?) AND home_area_type = ? AND age_bands IN (?) AND vehicle_type IN (?) AND vehicle_make IN (?) AND weather IN (?) AND road_type IN (?) AND speed_limit IN (?) AND light IN (?) AND road_surface IN (?) AND area_type IN (?) LIMIT ?, ?"
    transaction = "BEGIN TRANSACTION [search] BEGIN TRY " + query + " END TRY BEGIN CATCH ROLLBACK TRANSACTION [search] END CATCH END TRANSACTION [search]"    
    
    start_time = time.time()
    #result = execute_query(transaction)
    end_time = time.time()
    execution_time = end_time - start_time
    row_count = 1 # len(result)
    #if result is not None:
    with st.expander("✅ Result (" + str(row_count) + ")" , expanded=True):
        st.write("Executed in: " + str(execution_time) + "s")
        df = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))
        st.dataframe(df)
    # else:
    st.error("No result found. Please refine your search criteria.")

with tab1: # Search tab
    today = datetime.datetime.now()
    next_year = today.year + 1
    jan_1 = datetime.date(next_year, 1, 1)
    dec_31 = datetime.date(next_year, 12, 31)
    st.info("Search for data about traffical accidents in UK using our **relational database**.")
    
    search_form = st.form(key="search_form")
    with search_form:
        st.write("Select the search criteria below:")
        with st.expander("Accidents"):
            col1, col2 = st.columns(2)
            with col1:
                severity_selected = st.multiselect(
                    "Severity:",
                    ["Male", "Female", "Both", "Unknown"],
                )
            with col2:
                start_casualities_selected, end_casualities_selected = st.select_slider(
                    "Number of Casualties:",
                    options=[i for i in range(0, 101)],
                    value=(0, 100))
            timestamp_selected = st.date_input(
                "Select timestamp:",
                (jan_1, datetime.date(next_year, 1, 7)),
                jan_1,
                dec_31,
                format="MM.DD.YYYY",
            )
        with st.expander("Drivers involved in accidents"):
            col1, col2 = st.columns(2)
            with col1:
                sex_selected = st.multiselect(
                    "Sex:",
                    ["Male", "Female", "Both", "Unknown"],
                )
            with col2:
                home_area_type_selected = st.selectbox(
                    "Home area type:",
                    ["Urban", "Rural", "Unknown"],
                )
            age_bands_selected = st.multiselect("Age bands:",("Male", "Female", "Both"))               
        with st.expander("Vehicles involved in accidents"):  
            col1, col2 = st.columns(2)
            with col1:
                vehicle_type_selected = st.multiselect(
                    "Vehicle type:",
                    ["Car", "Van", "Lorry", "Motorcycle", "Bicycle", "Other", "Unknown"],
                )
            with col2:
                vehicle_make_selected = st.multiselect(
                    "Vehicle make:",
                    ["Ford", "Vauxhall", "Volkswagen", "BMW", "Peugeot", "Toyota", "Mercedes", "Audi", "Renault", "Other", "Unknown"],
                )
        with st.expander("Environment conditions"):
            col1, col2 = st.columns(2)
            with col1:
                weather_selected = st.multiselect(
                    "Weather:",
                    ["Fine no high winds", "Raining no high winds", "Snowing no high winds", "Fine + high winds", "Raining + high winds", "Snowing + high winds", "Fog or mist", "Other", "Unknown"],
                )
                road_type_selected = st.multiselect(
                    "Road type:",
                    ["Roundabout", "One way street", "Dual carriageway", "Single carriageway", "Slip road", "Unknown", "Other"],
                )
                speed_limit_selected = st.multiselect(
                    "Speed limit:",
                    ["20", "30", "40", "50", "60", "70", "Other", "Unknown"],
                )
            with col2:
                light_selected = st.multiselect(
                    "Light:",
                    ["Daylight", "Darkness - lights lit", "Darkness - lights unlit", "Darkness - no lighting", "Darkness - lighting unknown", "Other", "Unknown"],
                )
                road_surface_selected = st.multiselect(
                    "Road surface:",
                    ["Dry", "Wet or damp", "Snow", "Frost or ice", "Flood over 3cm. deep", "Oil or diesel", "Mud", "Other", "Unknown"],
                )
                area_type_selected = st.multiselect(
                    "Area type:",
                    ["Urban", "Rural", "Unknown"],
                )
        st.write("Select the data to be displayed:")
        with st.expander("Data rows and columns"):       
            start_row_selected, end_row_selected = st.select_slider(
                "Select a range of rows:",
                options=[i for i in range(0, 1201)],
                value=(0, 1200))
            columns_selected = st.multiselect(
                "Choose columns:",
                ["driver", "age", "location"]
            )
        submit = search_form.form_submit_button("Search", type="primary")
    if submit:
        st.write("Search results:")
        search()

with tab2: # Analyze tab
    with st.expander("Accidents"):
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
        st.line_chart(chart_data)
    with st.expander("Drivers involved in accidents"):
        st.info("put some data here...")
    with st.expander("Environment conditions"):
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
        st.bar_chart(chart_data)
    with st.expander("Locations", expanded=True):
        st.info("Click on the points to see information about the accident.")
        df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon'])
        st.map(df, size=2, use_container_width=False)

with tab3: # Monitoring tab
    st.write("Monitoring")











    #st.write("Home")
    #with st.expander("Table"):
    #    df = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))
    #    st.dataframe(df)

    #options = st.multiselect(
    #    "Select values:",
    #    ["Green", "Yellow", "Red", "Blue"],
    #)

    #option = st.selectbox("Choose a method:",("Create", "Read", "Update", "Delete"), index=None, placeholder="Select contact method...",)

    #st.button("Reset", type="primary")
    #st.button("Say hello")

    #today = datetime.datetime.now()
    #next_year = today.year + 1
    #jan_1 = datetime.date(next_year, 1, 1)
    #dec_31 = datetime.date(next_year, 12, 31)

    #d = st.date_input(
    #    "Select your vacation for next year",
    #    (jan_1, datetime.date(next_year, 1, 7)),
    #    jan_1,
    #    dec_31,
    #    format="MM.DD.YYYY",
    #)
    #d



