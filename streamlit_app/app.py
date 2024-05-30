import streamlit as st
import random
import time

def main():
    st.set_page_config(page_title="Hello", page_icon="👋")
    st.header('Home', divider='rainbow')
    st.info('Welcome to the home page. You can navigate to the chatbot or relational database pages using the sidebar.')

if __name__ == "__main__":
    main()