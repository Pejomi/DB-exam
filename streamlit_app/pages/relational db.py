import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.set_page_config(page_title="Relational DB", page_icon="🚦")

tab1, tab2, tab3 = st.tabs(["Search", "Analyze", "🔥Monitoring"])

def search():
    return "search"

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
                options = st.multiselect(
                    "Sex1:",
                    ["Male", "Female", "Both", "Unknown"],
                )
                options = st.multiselect(
                    "Age bands:",
                    ["16-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+", "Unknown"],
                )
            with col2:
                options = st.multiselect(
                    "Severity:",
                    ["Male", "Female", "Both", "Unknown"],
                )
                options = st.multiselect(
                    "Area:",
                    ["Male", "Female", "Both", "Unknown"],
                )
        with st.expander("Drivers involved in accidents"):
            col1, col2 = st.columns(2)
            with col1:
                options = st.multiselect(
                    "Sex:",
                    ["Male", "Female", "Both", "Unknown"],
                )
            with col2:
                option = st.selectbox("Age bands:",("Male", "Female", "Both"), index=None, placeholder="Select contact method...",)               
        with st.expander("Environment conditions"):
            col1, col2 = st.columns(2)
            with col1:
                options = st.multiselect(
                    "Weather:",
                    ["Fine no high winds", "Raining no high winds", "Snowing no high winds", "Fine + high winds", "Raining + high winds", "Snowing + high winds", "Fog or mist", "Other", "Unknown"],
                )
            with col2:
                options = st.multiselect(
                    "Light conditions:",
                    ["Daylight", "Darkness - lights lit", "Darkness - lights unlit", "Darkness - no lighting", "Darkness - lighting unknown", "Other", "Unknown"],
                )
        date = st.date_input(
            "Select datetime-stamp:",
            (jan_1, datetime.date(next_year, 1, 7)),
            jan_1,
            dec_31,
            format="MM.DD.YYYY",
        )
        
        start_color, end_color = st.select_slider(
            "Select a range of rows:",
            options=[i for i in range(0, 1201)],
            value=(0, 1200))

        columns = st.multiselect(
                    "Choose columns:",
                    ["driver", "age", "location"]
                )
        submit = search_form.form_submit_button("Search", type="primary")
    if submit:
        st.write("Search results:")
        
        with st.expander("✅ Result", expanded=True):
            df = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))
            st.dataframe(df)
        st.error("No result found. Please refine your search criteria.")

with tab2: # Analyze tab
    with st.expander("Drivers involved in accidents"):
        st.info("put some data here...")
    with st.expander("Environment conditions"):
        st.info("put some data here...")
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



