import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
from neo4j import GraphDatabase

st.set_page_config(page_title="Graph DB", page_icon="../img/logo.png")

if 'results' not in st.session_state:
    st.session_state.results = []

tab1, tab2, tab3 = st.tabs(["Search", "Analyze", "🔥Adminstrator"])

def search(tx, params):
    # Base query
    query = """
    MATCH (accident:Accident)-[:HAS_SEVERITY]->(severity:Severity),
          (accident)-[:DATE_WAS]->(date:Date),
          (accident)-[:HAS_SPEED_LIMIT]->(speedLimit:SpeedLimit),
          (accident)-[:ROAD_TYPE_WAS]->(roadType:RoadType),
          (accident)-[:WEATHER_WAS]->(weather:Weather),
          (accident)-[:LIGHT_WAS]->(light:Light),
          (accident)-[:ROAD_SURFACE_WAS]->(roadSurface:RoadSurface),
          (accident)-[:ACCIDENT_AREA_WAS]->(accidentArea:Area),
          (accident)-[:INVOLVES]->(vehicle:Vehicle)-[:HAS_VEHICLE_TYPE]->(vehicleType:VehicleType),
          (vehicle)-[:MADE_BY]->(make:Make),
          (vehicle)-[:DRIVEN_BY]->(driver:Driver)-[:HAS_SEX]->(sex:Sex),
          (driver)-[:HAS_AGE_BAND]->(ageBand:AgeBand),
          (driver)-[:LIVES_IN]->(driverArea:Area)
    WHERE date.date >= $start_date AND date.date <= $end_date AND
          accident.casualties >= $min_casualties AND accident.casualties <= $max_casualties
    """

    # Conditional clauses
    if 'severity' in params and params['severity']:
        query += "AND severity.level IN $severity "
    if 'sex' in params and params['sex']:
        query += "AND sex.type IN $sex "
    if 'driver_home_area' in params and params['driver_home_area']:
        query += "AND driverArea.area = $driver_home_area "
    if 'age_bands' in params and params['age_bands']:
        query += "AND ageBand.band IN $age_bands "
    if 'vehicle_types' in params and params['vehicle_types']:
        query += "AND vehicleType.type IN $vehicle_types "
    if 'vehicle_makes' in params and params['vehicle_makes']:
        query += "AND make.name IN $vehicle_makes "
    if 'weather' in params and params['weather']:
        query += "AND weather.condition IN $weather "
    if 'road_types' in params and params['road_types']:
        query += "AND roadType.type IN $road_types "
    if 'speed_limits' in params and params['speed_limits']:
        query += "AND speedLimit.limit IN $speed_limits "
    if 'light' in params and params['light']:
        query += "AND light.condition IN $light "
    if 'road_surfaces' in params and params['road_surfaces']:
        query += "AND roadSurface.condition IN $road_surfaces "
    if 'area_types' in params and params['area_types']:
        query += "AND accidentArea.area IN $area_types "

    # Return statement
    query += """
    RETURN accident, severity, date, speedLimit, roadType, weather, light, roadSurface, accidentArea, vehicle, vehicleType, make, driver, sex, ageBand, driverArea
    SKIP $skip LIMIT $limit
    """
    result = tx.run(query, params)
    return result.data()

def execute_query(params):
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "password"
    driver = GraphDatabase.driver(uri, auth=(user, password))

    with driver.session() as session:
        result = session.execute_read(search, params)
    
    driver.close()
    return result

with tab1: # Search tab
    today = datetime.datetime.now()
    next_year = today.year - 10
    jan_1 = datetime.date(next_year, 1, 1)
    dec_31 = datetime.date(next_year, 12, 31)
    st.info("Search for data about traffic accidents in UK using our **graph database**.")
    
    search_form = st.form(key="search_form")
    with search_form:
        st.write("Select the search criteria below:")
        with st.expander("Accidents"):
            col1, col2 = st.columns(2)
            with col1:
                severity_selected = st.multiselect(
                    "Severity:",
                    ["Fatal", "Serious", "Slight"],
                )
            with col2:
                start_casualties_selected, end_casualties_selected = st.select_slider(
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
                    ["Male", "Female", "Unknown"],
                )
            with col2:
                home_area_type_selected = st.selectbox(
                    "Home area type:",
                    ["Urban", "Rural", "Unknown"],
                )
            age_bands_selected = st.multiselect("Age bands:", ["0 - 5", "6 - 10", "11 - 15", "16 - 20", "21 - 25", "26 - 35", "36 - 45", "46 - 55", "56 - 65", "66 - 75", "Over 75", "No data"])    
        
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
                    ["FORD", "VAUXHALL", "VOLKSWAGEN", "BMW", "PEUGEOT", "TOYOTA", "MERCEDES", "AUDI", "RENAULT", "OTHER", "UNKNOWN"],
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
                    [20, 30, 40, 50, 60, 70],
                )
            with col2:
                light_selected = st.multiselect(
                    "Light:",
                    ["Daylight", "Darkness - lights lit", "Darkness - lights unlit", "Darkness - no lighting", "Darkness - lighting unknown", "Other", "Unknown"],
                )
                road_surface_selected = st.multiselect(
                    "Road surface:",
                    ["Dry", "Wet or damp", "Snow", "Frost or ice", "Flood over 3cm deep", "Oil or diesel", "Mud", "Other", "Unknown"],
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
                ["accident", "severity", "date", "speedLimit", "roadType", "weather", "light", "roadSurface", "accidentArea", "vehicle", "vehicleType", "make", "driver", "sex", "ageBand", "driverArea"]
            )
        submit = search_form.form_submit_button("Search", type="primary")
    if submit:
        st.write("Search results:")
        params = {
            "severity": severity_selected,
            "min_casualties": start_casualties_selected,
            "max_casualties": end_casualties_selected,
            "start_date": timestamp_selected[0].strftime("%Y-%m-%d"),
            "end_date": timestamp_selected[1].strftime("%Y-%m-%d"),
            "sex": sex_selected,
            "driver_home_area": home_area_type_selected,
            "age_bands": age_bands_selected,
            "vehicle_types": vehicle_type_selected,
            "vehicle_makes": vehicle_make_selected,
            "weather": weather_selected,
            "road_types": road_type_selected,
            "speed_limits": speed_limit_selected,
            "light": light_selected,
            "road_surfaces": road_surface_selected,
            "area_types": area_type_selected,
            "skip": start_row_selected,
            "limit": end_row_selected - start_row_selected
        }

        start_time = time.time()
        result = execute_query(params)
        end_time = time.time()
        execution_time = end_time - start_time
        row_count = len(result)
        if result:
            st.session_state.results = result
            with st.expander(f"✅ Result ({row_count})", expanded=True):
                st.write(f"Executed in: {execution_time:.2f}s")
                df = pd.DataFrame(result)
                st.dataframe(df)
        else:
            st.error("No result found. Please refine your search criteria.")

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
        if st.session_state.results:
            coordinates = []
            for entry in st.session_state.results:
                latitude = entry['accident']['latitude']
                longitude = entry['accident']['longitude']
                # Append the coordinates as a tuple to the coordinates list
                coordinates.append((latitude, longitude))

            df = pd.DataFrame(coordinates, columns=['lat', 'lon'])
            st.map(df, size=2, use_container_width=False)
   
with tab3: # Monitoring tab
    st.write("Monitoring")
