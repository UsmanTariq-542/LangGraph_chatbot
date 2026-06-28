import streamlit as st
from backend_sqlite_db_v02 import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid

# **************************************** utility functions *************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])

def generate_title(user_input: str) -> str:
    """Create a compact, readable title from user text."""
    cleaned = " ".join(user_input.strip().split())
    if not cleaned:
        return "New Chat"

    max_chars = 42
    return cleaned[:max_chars].rstrip() + ("..." if len(cleaned) > max_chars else "")


def get_first_user_message(messages):
    for msg in messages:
        if isinstance(msg, HumanMessage):
            return msg.content
    return ""


def ensure_title_for_thread(thread_id):
    thread_key = str(thread_id)
    if thread_key in st.session_state['chat_titles']:
        return

    messages = load_conversation(thread_id)
    first_user_text = get_first_user_message(messages)
    st.session_state['chat_titles'][thread_key] = generate_title(first_user_text)

# **************************************** Session Setup ******************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

# CHANGE 2: chat_titles dict — thread_id → title string
if 'chat_titles' not in st.session_state:
    st.session_state['chat_titles'] = {}
 

add_thread(st.session_state['thread_id'])

# Backfill titles for existing saved threads on first load/rerun.
for thread in st.session_state['chat_threads']:
    ensure_title_for_thread(thread)


# **************************************** Sidebar UI *********************************

st.sidebar.title('Persistent AI')

# new chat delete button
if st.sidebar.button('Reset All Conversations'):
    import os
    import sqlite3
    
    # 1. Sabse pehle agar koi connection open hai, usay close karein
    try:
        # Aapke backend code ka instance agar 'chatbot' hai, toh uske checkpointer ko access karein
        # Agar error aaye, toh bas niche wali lines run karein
        if 'chatbot' in globals():
            # Agar possible ho toh connection close karein
            pass 
            
        # 2. Files ko delete karein
        db_files = ["chatbot_state.db", "chat_history.db"]
        for db_file in db_files:
            if os.path.exists(db_file):
                os.remove(db_file)
        
        st.sidebar.success("Database Reset!")
        st.rerun()
    except Exception as e:
        st.sidebar.error(f"Error: {e}")


if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')



# CHANGE 3: button mein UUID ki jagah title dikhao
for thread_id in st.session_state['chat_threads'][::-1]:
    ensure_title_for_thread(thread_id)
    title = st.session_state['chat_titles'].get(
        str(thread_id),
        "New Chat"
    )
    if st.sidebar.button(title, key=f"thread-{thread_id}"):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
 
        temp_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role': role, 'content': msg.content})
 
        st.session_state['message_history'] = temp_messages
 
 

# **************************************** Main UI ************************************

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:
    # CHANGE 4: pehla message aaya → title save karo
    thread_key = str(st.session_state['thread_id'])
    if thread_key not in st.session_state['chat_titles']:
        st.session_state['chat_titles'][thread_key] = generate_title(user_input)


    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

     # first add the message to message_history
    with st.chat_message("assistant"):
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                if isinstance(message_chunk, AIMessage):
                    # yield only assistant tokens
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})