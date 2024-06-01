import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
from neo4j import GraphDatabase

st.set_page_config(page_title="Graph DB", page_icon="../img/logo.png")

tab1, tab2, tab3 = st.tabs(["Search", "Analyze", "🔥Adminstrator"])

def search(tx, params):
    # Base query
    query = """
    MATCH (accident:Accident)-[:HAS_SEVERITY]->(severity:Severity)
    MATCH (accident)-[:DATE_WAS]->(date:Date)
    MATCH (accident)-[:INVOLVES]->(vehicle:Vehicle)-[:HAS_VEHICLE_TYPE]->(vehicleType:VehicleType)
    MATCH (vehicle)-[:MADE_BY]->(make:Make)
    MATCH (vehicle)-[:DRIVEN_BY]->(driver:Driver)-[:HAS_SEX]->(sex:Sex)
    MATCH (driver)-[:HAS_AGE_BAND]->(ageBand:AgeBand)
    WHERE date.date >= $start_date AND date.date <= $end_date
    """

    # Conditional clauses
    if 'severity' in params and params['severity']:
        query += "AND severity.level IN $severity "
    if 'vehicle_types' in params and params['vehicle_types']:
        query += "AND vehicleType.type IN $vehicle_types "
    if 'vehicle_makes' in params and params['vehicle_makes']:
        query += "AND make.name IN $vehicle_makes "

    # Return and pagination
    query += """
    RETURN accident, severity, date, vehicle, vehicleType, make, driver, sex, ageBand
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

            timestamp_selected = st.date_input(
                "Select timestamp:",
                (jan_1, datetime.date(next_year, 1, 7)),
                jan_1,
                dec_31,
                format="MM.DD.YYYY",
            )
                       
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
        
        st.write("Select the data to be displayed:")
        with st.expander("Data rows and columns"):       
            start_row_selected, end_row_selected = st.select_slider(
                "Select a range of rows:",
                options=[i for i in range(0, 1201)],
                value=(0, 1200))
           
        submit = search_form.form_submit_button("Search", type="primary")
    if submit:
        st.write("Search results:")
        params = {
            "severity": severity_selected,
            "start_date": timestamp_selected[0].strftime("%Y-%m-%d"),
            "end_date": timestamp_selected[1].strftime("%Y-%m-%d"),
            "vehicle_types": vehicle_type_selected,
            "vehicle_makes": vehicle_make_selected,
            "skip": start_row_selected,
            "limit": end_row_selected - start_row_selected
        }

        start_time = time.time()
        result = execute_query(params)
        end_time = time.time()
        execution_time = end_time - start_time
        row_count = len(result)
        if result:
            with st.expander(f"✅ Result ({row_count})", expanded=True):
                st.write(f"Executed in: {execution_time:.2f}s")
                df = pd.DataFrame(result)
                st.dataframe(df)
        else:
            st.error("No result found. Please refine your search criteria.")

with tab2: # Analyze tab
    st.write("put some data here...")
   
with tab3: # Monitoring tab
    st.write("Monitoring")
