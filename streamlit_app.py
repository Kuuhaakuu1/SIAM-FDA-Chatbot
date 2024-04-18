import os.path
import os
import streamlit as st
import numpy as np
import pickle
from streamlit_extras.add_vertical_space import add_vertical_space 
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
from llama_index.core  import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
#################################################################
def load_translations(file_path):
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("The file was not found.")
        return {}

translations = load_translations('translations.pkl')
# Toggle language function
def toggle_language():
    st.session_state.toggle = not st.session_state.toggle
    # Reset the initial message with the new language
    st.session_state.messages = [{"role": "assistant", "content": translations['fr' if st.session_state.toggle else 'ar']['initial_message']}]

# Initialize the session state for toggle if it's not already there
if 'toggle' not in st.session_state:
    st.session_state.toggle = True  # True for English, False for Arabic

# Initialize messages if not present
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": translations['fr' if st.session_state.toggle else 'ar']['initial_message']}]

current_lang = 'fr' if st.session_state.toggle else 'ar'
#################################################################
path = "data"

# Sidebar contents
with st.sidebar:
    st.button(
        label=translations[current_lang]['language'],
        on_click=toggle_language
    )
    st.title(translations[current_lang]['title'])
    st.markdown(translations[current_lang]['about_us_description'])
    st.write(translations[current_lang]['created_by'])
    st.image("./assets/logo-large-pole-digital-light.png")

# Main page contents
col1, col2, col3, col4, col5 = st.columns([0.5,0.8,0.8,0.8,5])
col1.image("./assets/logo-large-pole-digital-light.png", width=117)
col3.image("./assets/IAV_White.png", width=50)
col4.image("./assets/ONCA1 (Custom).png", width=50)
col5.image("./assets/ONSSA (Custom).png", width=50)

st.title(translations[current_lang]['discover_financial_aid'])

@st.cache_resource(show_spinner=False)
def load_index():
    with st.spinner(text="جاري تحميل المستندات انتظر قليلاً! قد يستغرق هذا الأمر من 1 إلى 2 دقيقة."):
        if not os.path.exists("./storage"):
            # load the documents and create the index
            documents = SimpleDirectoryReader(path).load_data()
            index = VectorStoreIndex.from_documents(documents)
            # store it for later
            index.storage_context.persist()
        else:
            # load the existing index
            storage_context = StorageContext.from_defaults(persist_dir="./storage")
            index = load_index_from_storage(storage_context)
        return index
index = load_index()


# Handling chat interactions
if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [{"role": "assistant",  "content": translations[current_lang]['initial_message']}]
    
if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_plus_context", verbose=True, system_prompt=("If you need aditional information, ask for it."))

if prompt := st.chat_input(translations[current_lang]['enter_your_question']):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner(translations[current_lang]['thinking']):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history