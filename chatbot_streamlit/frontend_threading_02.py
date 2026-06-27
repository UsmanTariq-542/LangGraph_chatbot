import streamlit as st
from backend import chatbot,model
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

# CHANGE 1: generating a unique title from the first chat message
def generate_title(user_input: str) -> str:
    """LLM se 5-6 word ka meaningful title banwao"""
    response = model.invoke([
        HumanMessage(content=(
            f"Generate a short 5-6 word title for a chat that starts with this message. "
            f"Return ONLY the title, nothing else, no quotes, no punctuation at end.\n\n"
            f"Message: {user_input[:500]}"  # max 500 chars bhejo — zyada nahi chahiye
        ))
    ])
    return response.content.strip()

# **************************************** Session Setup ******************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

# CHANGE 2: chat_titles dict — thread_id → title string
if 'chat_titles' not in st.session_state:
    st.session_state['chat_titles'] = {}
 

add_thread(st.session_state['thread_id'])


# **************************************** Sidebar UI *********************************

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

# for thread_id in st.session_state['chat_threads'][::-1]:
#     if st.sidebar.button(str(thread_id)):
#         st.session_state['thread_id'] = thread_id
#         messages = load_conversation(thread_id)

#         temp_messages = []

#         for msg in messages:
#             if isinstance(msg, HumanMessage):
#                 role='user'
#             else:
#                 role='assistant'
#             temp_messages.append({'role': role, 'content': msg.content})

#         st.session_state['message_history'] = temp_messages


# CHANGE 3: button mein UUID ki jagah title dikhao
for thread_id in st.session_state['chat_threads'][::-1]:
    title = st.session_state['chat_titles'].get(
        str(thread_id),
        f"Chat {str(thread_id)[:8]}..."  # fallback: pehla message aane se pehle
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
        with st.spinner(""):
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