import streamlit as st
import random
import time

def main():
    st.set_page_config(page_title="SafeWay", page_icon="../img/logo.png")
    col1, col2 = st.columns([0.8, 8])
    with col1:
        col1.markdown("<div style='width: 1px; height: 18px'></div>", unsafe_allow_html=True)
        
        st.image("../img/logo.png", width=50)
    with col2:  
        st.title("SafeWay")
   
    st.write("SafeWay is a platform that provide tools to predict and prevent car accidents.")
    
    st.info('To start using our platform, please login with your email address below.')
    form = st.form(key='login_form')
    name = form.text_input(label="Enter email:", placeholder="Type here ...")
    submit = form.form_submit_button(label='Login')
    #if submit:
    #    login(name)

if __name__ == "__main__":
    main()