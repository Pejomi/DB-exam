import streamlit as st
import random
import time
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

st.set_page_config(page_title="Chatbot", page_icon="../img/logo.png")

def connect_to_mongodb():
    cluster = MongoClient(os.getenv("MONGODB"))
    db = cluster["chatbot"]
    collection = db["messages"]
    return collection

def save_chat(chat):
    try:
        collection = connect_to_mongodb()
        collection.insert_one(chat)
        st.toast("Chat history saved successfully.", icon="✅")
    except pymongo.errors.DuplicateKeyError:
        st.error("Chat history with this title already exists. Please choose another title.")
        

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
    # connection = connect_to_mongodb()
    # connection.create_index([("email", pymongo.ASCENDING), ("title", pymongo.ASCENDING)], unique=True)
    st.rerun()

def find_all_titles_by_email(email):
    collection = connect_to_mongodb()
    result = collection.aggregate([{"$match": {"email": email}}, {"$group": {"_id": "$title"}}])
    return result

def find_user_chat_by_title(email, title):
    collection = connect_to_mongodb()
    result = collection.find({"email": email, "title": title})  
    return result

def find_all_chats():
    collection = connect_to_mongodb()
    result = collection.aggregate([{"$group": {"_id": "$email", "titles": {"$push": "$title"}, "messages": {"$push": "$messages"}}}])
    return result

def find_all_chats_by_email(email):
    collection = connect_to_mongodb()
    result = collection.aggregate([{"$match": {"email": email}}, {"$group": {"_id": "$title", "messages": {"$push": "$messages"}}}])
    return result

def clear_chat():
    st.session_state.messages[0] = []
    st.rerun()

def delete_chat(email, title):
    collection = connect_to_mongodb()
    collection.delete_one({"email": email, "title": title})
    st.toast("Chat history deleted successfully.", icon="🗑️")
    st.rerun()
    

def update_chat(email, title, messages):
    collection = connect_to_mongodb()
    collection.update_one({"email": email, "title": title}, {"$set": {"messages": messages}})

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
    if st.session_state.email == "admin":
        tab1, tab2, tab3 = st.tabs(["Chat", "Saved messages", "🔥Adminstrator"])
        with tab3: # Admin tab
            all_user_chats = list(find_all_chats())
            if len(all_user_chats) == 0:
                st.info("No chat history found.")
                st.stop()

            # Display chat statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(label="Total Users", value=len(all_user_chats))
            with col2:
                st.metric(label="Total Chats", value=sum([len(chat["titles"]) for chat in all_user_chats]))
            with col3:
                sum_of_messages = sum([sum([len(message) for message in chat["messages"]]) for chat in all_user_chats])
                st.metric(label="Total Messages", value=sum_of_messages)
            with col4:
                avg_messages_in_one_chat = round(sum([sum([len(message) for message in chat["messages"]]) for chat in all_user_chats]) / sum([len(chat["messages"]) for chat in all_user_chats]))
                st.metric(label="Avg messages in a chat", value=avg_messages_in_one_chat)

            # Display all users in a table
            with st.expander("All users"):
                st.table(pd.DataFrame({"User": [chat["_id"] for chat in all_user_chats], "Titles (count)": [len(chat["titles"]) for chat in all_user_chats], "Messages (count)": [len(chat["messages"]) for chat in all_user_chats]}))

            # Search for user chat
            col1, col2 = st.columns([8, 1.05])
            with col1:
                email = st.text_input("Search for user chat:", placeholder="Type user email ...")
            with col2:
                col2.markdown("<div style='width: 1px; height: 29px'></div>", unsafe_allow_html=True)
                search = st.button("Search", type="primary")
            if search:
                if email.strip() == "":
                    st.error("Please enter a valid email address.")
                else:
                    result = list(find_all_chats_by_email(email))
                    if len(result) > 0:
                        for chat in result:
                            with st.expander(chat["_id"]):
                                for message in chat["messages"][0]:
                                    with st.chat_message(message["role"]):
                                        st.markdown(message["content"])
                    else:
                        st.info("No chat history found for this email address.")
    else:
        tab1, tab2= st.tabs(["Chat", "Saved messages"])
    
    with tab1: # Chat tab
        messages = st.session_state.messages[0] # Current chat messages
        # Save and clear buttons
        col1, col2, col3 = st.columns([9, 1.45, 1.25])
        with col2:
            with st.popover("Save"):
                st.write("Save in Mongo DB 📂")
                title = st.text_input("Name your chat-history:", placeholder="Type here ...") 
                if st.button("Save"):
                    chat = {"email": st.session_state.email, "title": title, "messages": messages}
                    save_chat(chat)
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
        if len(list(find_all_titles_by_email(st.session_state.email))) == 0:
            st.info("No saved chat history found.")
            st.stop()
        else:
            col1, col2 = st.columns([8,1])
            with col1:
                # Select saved chat to be displayed
                title = st.selectbox("Select chat:", [chat["_id"] for chat in find_all_titles_by_email(st.session_state.email)], index=None, placeholder="Select chat ...")
                if title:
                    st.session_state.messages[1] = list(find_user_chat_by_title(st.session_state.email, title))[0]["messages"]
                else:
                    st.session_state.messages[1] = []
            with col2:
                # Delete selected chat
                col2.markdown("<div style='width: 1px; height: 29px'></div>", unsafe_allow_html=True)
                if st.button("Delete", type="primary", disabled=not title):
                    delete_chat(st.session_state.email, title)

            # Display selected chat
            messages = st.session_state.messages[1] # Saved chat messages
            tab_container = tab2.container(height=615, border=False)
            with tab_container:
                for message in messages:
                    with tab_container.chat_message(message["role"]):
                        st.markdown(message["content"])

            if prompt := st.chat_input("Type your message", key="saved_chat", disabled=not title):
                messages.append({"role": "user", "content": prompt})
                with tab_container.chat_message("user"):
                    st.markdown(prompt)
                with tab_container.chat_message("assistant"):
                    response = st.write_stream(response_generator())
                messages.append({"role": "assistant", "content": response})
                update_chat(st.session_state.email, title, messages) # Update the saved chat history