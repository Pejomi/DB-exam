import streamlit as st
import random
import time
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
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
            "Hello there! How can I assist you today?",
            "Hi, human! Is there human! Is there anything I can help you with? Hi, human! Is there anything I can help you with? Hi, human! Is there anything I can help you with? Hi, human! Is there anything I can help you with? ",
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
    form = st.form(key='my-form')
    name = form.text_input(label="Enter email:", placeholder="Type here ...")
    submit = form.form_submit_button(label='Login')
    if submit:
        login(name)
    
def login(email):
    if email.strip() == "":
        st.error("Please enter a valid email address.")
        return
    st.session_state.email = email
    st.session_state.messages = []
    st.rerun()

def find_all_user_titles(email):
    collection = connect_to_mongodb()
    result = collection.find({"email": email})  
    return result

def find_user_chat(email, title):
    collection = connect_to_mongodb()
    result = collection.find({"email": email, "title": title})  
    return result

def reset_chat():
    st.session_state.messages = []
    st.rerun()

st.markdown(
    """
        <style>
            .st-emotion-cache-janbn0 {
                flex-direction: row-reverse;
                text-align: justify;
                text-align-last: right;
                -moz-text-align-last: right;
                background-color: transparent;
            }
            .st-emotion-cache-4oy321 {
                background-color: rgba(38, 39, 48, 0.5);
                padding: 1rem;
            }
        </style>
    """,
    unsafe_allow_html=True,
)
if "email" not in st.session_state or st.session_state.email is None:
        setup()
else:
    tab1, tab2 = st.tabs(["Chat", "Saved messages"])
    with tab1:
        st.session_state.chat_open = True

    with tab2:
        title = st.selectbox("Select chat:", find_all_user_titles(st.session_state.email), placeholder="No chat selected", index=None)
   

if "chat_open" in st.session_state and st.session_state.chat_open == True:
# Initialize chat history
    messages = st.container()
    with messages:
        col1, col2 = st.columns([9, 1.25])
        with col2:
            with st.popover("Save"):
                st.write("Save in Mongo DB 📂")
                name = st.text_input("Name your chat-history:", placeholder="Type here ...")
                save = st.button("Save")
                if save:
                    history = {"email": st.session_state.email, "title": name, "messages": st.session_state.messages}
                    insert_chat_history(history)

        # Chat first message
        messages.chat_message("assistant").write("Hello! How can I help you today?")

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Accept user input
    if prompt := st.chat_input("Type your message"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator())
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# Todo:
# - show selectbox with options of previous chats or create new chat with new title
# - show chat history