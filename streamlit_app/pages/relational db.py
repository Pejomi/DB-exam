import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.set_page_config(page_title="Relational DB", page_icon="🚦")

st.header("Relational Database", divider='rainbow')

with st.expander("Table"):
    df = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))
    st.dataframe(df)

options = st.multiselect(
    "Select values:",
    ["Green", "Yellow", "Red", "Blue"],
    )

option = st.selectbox(
    "Choose a method:",
    ("Create", "Read", "Update", "Delete"), index=None, placeholder="Select contact method...",)

st.button("Reset", type="primary")
st.button("Say hello")

today = datetime.datetime.now()
next_year = today.year + 1
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

d = st.date_input(
    "Select your vacation for next year",
    (jan_1, datetime.date(next_year, 1, 7)),
    jan_1,
    dec_31,
    format="MM.DD.YYYY",
)
d