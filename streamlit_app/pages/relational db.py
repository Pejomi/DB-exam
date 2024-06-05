import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from get_db_conn import get_db_conn

# error handling for all queries, only fetch once refetch when something changes, choose all from start
st.set_page_config(page_title="Relational DB", page_icon="../img/logo.png")

tab1, tab2, tab3 = st.tabs(["Search", "Analyze", "🔥Adminstrator"])

def get_severity_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getSeverities", cnxn)
    return result["type"].tolist()

def get_max_casualties():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getMaxCasualties", cnxn)
    return result["max_casualties"].tolist()

def get_max_and_min_dates():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getMaxAndMinDates", cnxn)
    return result

def get_hit_object_in_carriage_way_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getHitObjectInCarriageway", cnxn)
    return result["hit_object_in_carriageway"].tolist()

def get_hit_object_off_carriage_way_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getHitObjectOffCarriageway", cnxn)
    return result["hit_object_off_carriageway"].tolist()

def get_vehicle_manoeuvre_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getVehicleManoeuvre", cnxn)
    return result["vehicle_manoeuvre"].tolist()

def get_point_of_impact_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getPointOfImpacts", cnxn)
    return result["point_of_impact"].tolist()

def get_sex_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getSex", cnxn)
    return result["sex"].tolist()

def get_age_bands_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getAgeBands", cnxn)
    return result["band"].tolist()

def get_area_types_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getAreaTypes", cnxn)
    return result["type"].tolist()

def get_vehicle_make_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getVehicleMake", cnxn)
    return result["make"].tolist()

def get_vehicle_model_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getVehicleModel", cnxn)
    return result["model"].tolist()

def get_vehicle_type_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getVehicleType", cnxn)
    return result["type"].tolist()

def get_vehicle_model_year_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getVehicleModelYear", cnxn)
    return result["model_year"].tolist()

def get_weather_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getWeather", cnxn)
    return result["weather"].tolist()

def get_road_type_options():    
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getRoadTypes", cnxn)
    return result["road_type"].tolist()

def get_speed_limit_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getSpeedLimits", cnxn)
    return result["speed_limit"].tolist()

def get_light_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getLights", cnxn)
    return result["light"].tolist()

def get_road_surface_options():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getRoadSurfaces", cnxn)
    return result["road_surface"].tolist()

def count_rows():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.countRows", cnxn)
    return result["count"].tolist()

def get_all_columns():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getAllColumns", cnxn)
    return result.columns.tolist()

def get_all_data():
    cnxn = get_db_conn()
    result = pd.read_sql("EXECUTE dbo.getAllData", cnxn)
    return result

def search():
    # make a query to the database with transaction  
    query = "SELECT "
    data = st.session_state.selected_options
    fields = ", ".join(data["columns"]) if len(data["columns"]) > 0 else "*"
    #order = "WITH a AS (SELECT *, ROW_NUMBER() OVER (ORDER BY date) AS row_num FROM dbo.ViewAll) SELECT * FROM a "
    where_clause = []
    values = []
    for key, value in data.items():
        if key == "dates":
            where_clause.append("date BETWEEN ? AND ?")
            values.append(value[0])
            values.append(value[1])
        
        if type(value) == list and len(value) > 0:
            if key == "casualties":
                where_clause.append("number_of_casualties BETWEEN ? AND ?")
                values.append(value[0])
                values.append(value[1]) 
            elif key == "rows":
                #where_clause.append("a.row_num BETWEEN ? AND ?")
                #values.append(value[0])
                #values.append(value[1])
                pass
            elif key == "columns":
                pass
            else:
                where_clause.append(str(key) + " IN (%s)" % (', '.join('?' for i in range(len(value)))))
                for v in value:
                    values.append(v)
            
    query = f"SELECT {fields} FROM dbo.ViewAll"
    query = query + " WHERE " + " AND ".join(where_clause) if len(where_clause) > 0 else query
    transaction = "BEGIN TRANSACTION [search] BEGIN TRY " + query + " END TRY BEGIN CATCH ROLLBACK TRANSACTION [search] END CATCH"

    try:
        start_time= time.time()
        cnxn = get_db_conn()
        cursor = cnxn.cursor()
        result = pd.read_sql(query, cnxn, params=(tuple(values)))
        end_time = time.time()
        execution_time = round(end_time - start_time)

        if result.shape[0] == 0:
            st.info("No result found. Please refine your search criteria.")
        else:
            with st.expander("✅ Result (" + str(result.shape[0]) + " rows)", expanded=True):
                st.write("Executed in: " + str(execution_time) + "s")
                st.dataframe(result)
    except:
        st.error("An error occurred while fetching the data. Please try again.")

if "selected_options" not in st.session_state:
    st.session_state.selected_options = {
        "severity_type": [],
        "casualties": [0, get_max_casualties()[0]],
        "dates": (get_max_and_min_dates()["min_date"][0], get_max_and_min_dates()["max_date"][0]),
        "hit_object_in_carriageway": [],
        "hit_object_off_carriageway": [],
        "vehicle_manoeuvre": [],
        "point_of_impact": [],
        "sex": [],
        "home_area_type": [],
        "bands": [],
        "make": [],
        "model": [],
        "vehicle_type": [],
        "model_year": [],
        "weather": [],
        "road_type": [],
        "speed_limit": [],
        "light": [],
        "road_surface": [],
        "area_type": [],
        "columns": get_all_columns(),
        "rows": [0, count_rows()[0]],
    }

with tab1: # Search tab   
    st.info("Search for data about traffical accidents in UK using our **relational database**.")
    search_form = st.form(key="search_form")
    with search_form:
        st.write("Select the search criteria below:")
        with st.expander("Accidents"):
            col1, col2 = st.columns(2)
            with col1:
                severity_selected = st.multiselect(
                    "Severity:",
                    get_severity_options()
                )
            with col2:
                start_casualties_selected, end_casualties_selected = st.select_slider(
                    "Number of Casualties:",
                    options=[i for i in range(0, get_max_casualties()[0] + 1)],
                    value=(0, get_max_casualties()[0]))
            dates_selected = st.date_input(
                "Select dates:",
                (get_max_and_min_dates()["min_date"][0], get_max_and_min_dates()["max_date"][0]),
                get_max_and_min_dates()["min_date"][0],
                get_max_and_min_dates()["max_date"][0],
                format="MM.DD.YYYY",
            )
        with st.expander("Collisions"):
            col1, col2 = st.columns(2)
            with col1:
                hit_object_in_selected = st.multiselect(
                    "Hit object in carriage way:",
                    get_hit_object_in_carriage_way_options()
                )
                vehicle_manoevre_selected = st.multiselect(
                    "Vehicle manoeuvre:",
                    get_vehicle_manoeuvre_options()
                )
            with col2:
                hit_object_off_selected = st.multiselect(
                    "Hit object off carriage way:",
                    get_hit_object_off_carriage_way_options()
                )
                point_of_impact_selected = st.multiselect(
                    "Point of impact:",
                    get_point_of_impact_options()
                )
        with st.expander("Drivers involved in accidents"):
            col1, col2 = st.columns(2)
            with col1:
                sex_selected = st.multiselect(
                    "Sex:",
                    get_sex_options()
                )
            with col2:
                home_area_type_selected = st.multiselect(
                    "Home area type:",
                    get_area_types_options()
                )
            age_bands_selected = st.multiselect("Age bands:", get_age_bands_options())               
        with st.expander("Vehicles involved in accidents"):  
            col1, col2 = st.columns(2)
            with col1:
                vehicle_make_selected = st.multiselect(
                    "Make:",
                    get_vehicle_make_options()
                )
                vehicle_model_selected = st.multiselect(
                    "Model:",
                    get_vehicle_model_options()
                )
            with col2:
                vehicle_type_selected = st.multiselect(
                    "Vehicle type:",
                    get_vehicle_type_options()
                )
                vehicle_model_year_selected = st.multiselect(
                    "Model year:",
                    get_vehicle_model_year_options()
                )
        with st.expander("Environment conditions"):
            col1, col2 = st.columns(2)
            with col1:
                weather_selected = st.multiselect(
                    "Weather:",
                    get_weather_options()
                )
                road_type_selected = st.multiselect(
                    "Road type:",
                    get_road_type_options()
                )
                speed_limit_selected = st.multiselect(
                    "Speed limit:",
                    get_speed_limit_options()
                )
            with col2:
                light_selected = st.multiselect(
                    "Light:",
                    get_light_options()
                )
                road_surface_selected = st.multiselect(
                    "Road surface:",
                    get_road_surface_options()
                )
                area_type_selected = st.multiselect(
                    "Area type:",
                    get_area_types_options()
                )
        st.write("Select the data to be displayed:")
        with st.expander("Data rows and columns"):       
            start_row_selected, end_row_selected = st.select_slider(
                "Select a range of rows:",
                options=[i for i in range(0, count_rows()[0] + 1)],
                value=(0, count_rows()[0]))
            columns_selected = st.multiselect(
                "Choose columns:",
                get_all_columns()
            )        
        st.session_state.selected_options = {
            "severity_type": severity_selected,
            "casualties": [start_casualties_selected, end_casualties_selected],
            "dates": dates_selected,
            "hit_object_in_carriageway": hit_object_in_selected,
            "hit_object_off_carriageway": hit_object_off_selected,
            "vehicle_manoeuvre": vehicle_manoevre_selected,
            "point_of_impact": point_of_impact_selected,
            "sex": sex_selected,
            "home_area_type": home_area_type_selected,
            "bands": age_bands_selected,
            "make": vehicle_make_selected,
            "model": vehicle_model_selected,
            "vehicle_type": vehicle_type_selected,
            "model_year": vehicle_model_year_selected,
            "weather": weather_selected,
            "road_type": road_type_selected,
            "speed_limit": speed_limit_selected,
            "light": light_selected,
            "road_surface": road_surface_selected,
            "area_type": area_type_selected,
            "columns": columns_selected,
            "rows": [start_row_selected, end_row_selected],
        }
        submit = search_form.form_submit_button("Search", type="primary")
    if submit:
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
    # Display chat statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Severities", value=len(get_severity_options()))
    with col2:
        st.metric(label="Total Chats", value=10)
    with col3:
        st.metric(label="Total Messages", value=10)
    with col4:
        st.metric(label="Avg messages in a chat", value=10)
