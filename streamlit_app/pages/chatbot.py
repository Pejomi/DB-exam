import streamlit as st
import random
import time
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Chatbot", page_icon="🤖")

def connect_to_mongodb():
    cluster = MongoClient(os.getenv("MONGODB"))
    db = cluster["chatbot"]
    collection = db["messages"]
    return collection

def insert_chat_history(chat_history):
    collection = connect_to_mongodb()
    collection.insert_one(chat_history)

# Streamed response emulator
def response_generator(): # TODO: Implement a real chatbot
    response = random.choice(
        [
            "How can I help you today?",
            "What can I do for you today?",
            "I'm sorry, I don't understand. Can you rephrase that?",
            "Hello there! How can I assist you today?",
            "Do you need help?",
        ]
    )
    # Emulate delay
    for word in response.split():
        yield word + " "
        time.sleep(0.10)

# Login form to get user email before starting chat
def setup():
    st.info('To start using the chatbot, please login with your email address below. Your email address will be used to save your chat history.')
    form = st.form(key='login_form')
    name = form.text_input(label="Enter email:", placeholder="Type here ...")
    submit = form.form_submit_button(label='Login')
    if submit:
        login(name)
    
def login(email):
    if email.strip() == "":
        st.error("Please enter a valid email address.")
        return
    st.session_state.email = email
    st.session_state.messages = [[], []] # index 0 for new chat, index 1 for saved chat
    st.rerun()

def find_all_user_titles():
    collection = connect_to_mongodb()
    result = collection.find({"email": st.session_state.email})  
    return result

def find_user_chat(title):
    collection = connect_to_mongodb()
    result = collection.find({"email": st.session_state.email, "title": title})  
    return result

def clear_chat():
    st.session_state.messages[0] = []
    st.rerun()

def delete_chat(title):
    collection = connect_to_mongodb()
    collection.delete_one({"email": st.session_state.email, "title": title})
    st.rerun()

def update_chat(title):
    collection = connect_to_mongodb()
    collection.update_one({"email": st.session_state.email, "title": title}, {"$set": {"messages": st.session_state.messages[1]}})

st.markdown(
    """
        <style>
            .st-emotion-cache-janbn0 {
                flex-direction: row-reverse;
                text-align: justify;
                text-align-last: right;
                -moz-text-align-last: right;
            }
            .st-emotion-cache-1c7y2kd {
                flex-direction: row-reverse;
                text-align: justify;
                text-align-last: right;
                -moz-text-align-last: right;
            }
            .st-emotion-cache-4oy321 {
                padding: 1rem;
            }
             .st-emotion-cache-13ln4jf {
                height: 100vh;
            }
        </style>
    """,
    unsafe_allow_html=True,
)

if "email" not in st.session_state:
    setup() # Login setup
else:
    tab1, tab2 = st.tabs(["Chat", "Saved messages"])

    with tab1: # Chat tab
        messages = st.session_state.messages[0] # Current chat messages
        # Save and clear buttons
        col1, col2, col3 = st.columns([9, 1.45, 1.25])
        with col2:
            with st.popover("Save"):
                st.write("Save in Mongo DB 📂")
                name = st.text_input("Name your chat-history:", placeholder="Type here ...") 
                if st.button("Save"):
                    history = {"email": st.session_state.email, "title": name, "messages": messages}
                    insert_chat_history(history)
        with col3:
            if st.button("Clear", type="primary"):
                clear_chat()
        # Display chat messages
        tab_container = tab1.container(height=645, border=False)
        with tab_container:
            # First message from chatbot
            first_message = "Hello! How can I help you today?"
            if "assistant" not in [message["role"] for message in messages]:
                messages.append({"role": "assistant", "content": first_message})
            #messages.append({"role": "assistant", "content": first_message})
            
            # Display chat messages
            for message in messages:
                with tab_container.chat_message(message["role"]):
                    st.markdown(message["content"])
        # Chat message input
        if prompt := st.chat_input("Type your message",key="new_chat"):
            # Save user message to session state
            messages.append({"role": "user", "content": prompt})
            with tab_container.chat_message("user"):
                st.markdown(prompt)
            # Generate chatbot response and save to session state
            with tab_container.chat_message("assistant"):
                response = st.write_stream(response_generator())
            messages.append({"role": "assistant", "content": response})

    with tab2: # Saved messages tab
        if len([chat["title"] for chat in find_all_user_titles()]) == 0:
            st.info("No saved chat history found.")
            st.stop()
        else:
            col1, col2 = st.columns([8,1])
            with col1:
                # Select saved chat to be displayed
                chat = st.selectbox("Select chat:", [chat["title"] for chat in find_all_user_titles()], placeholder="No chat selected", index=None)
                if chat:
                    st.session_state.messages[1] = list(find_user_chat(chat))[0]["messages"]
                else:
                    st.session_state.messages[1] = []
            with col2:
                # Delete selected chat
                col2.markdown("<div style='width: 1px; height: 29px'></div>", unsafe_allow_html=True)
                if st.button("Delete", type="primary", disabled=not chat):
                    delete_chat(chat)

            # Display selected chat
            messages = st.session_state.messages[1] # Saved chat messages
            tab_container = tab2.container(height=615, border=False)
            with tab_container:
                for message in messages:
                    with tab_container.chat_message(message["role"]):
                        st.markdown(message["content"])

            if prompt := st.chat_input("Type your message", key="saved_chat", disabled=not chat):
                messages.append({"role": "user", "content": prompt})
                with tab_container.chat_message("user"):
                    st.markdown(prompt)
                with tab_container.chat_message("assistant"):
                    response = st.write_stream(response_generator())
                messages.append({"role": "assistant", "content": response})
                update_chat(chat) # Update the saved chat history