import os.path
import os
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space 
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
from llama_index.core  import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

path = "data"

# Side bar contents
with st.sidebar:
    st.title('الذكاء الاصطناعي أشبال')
    st.markdown('''
    ## معلومات عنا:
    هذا التطبيق هو تواصل مع الذكاء الاصطناعي أشبال مدعومة ب (LLM) تم بناؤه باستخدام:
    - [Streamlit](https://streamlit.io/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM Model
    - [Idarati dataset](https://www.idarati.ma/)
    ''')
    add_vertical_space(5)
    st.write('تم إنشاؤه من قبل فريق أشبال')
st.title('تواصل مع الذكاء الاصطناعي أشبال')



if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant",  "content": "اسألني سؤالاً حول مكتبة مستندات مفتوحة المصدر Idarati !"}
    ]



@st.cache_resource(show_spinner=False)
def load_index():
    with st.spinner(text="جاري تحميل  مستندات اداراتي  انتظر قليلاً! قد يستغرق هذا الأمر من 1 إلى 2 دقيقة."):
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


if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
# either way we can now query the index
# query_engine = index.as_query_engine()

if prompt := st.chat_input(" أدخل سؤالك هنا"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("جارٍ التفكير..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history        
# query = st.text_input("What would you like to know about your PDF?")
    
# if query:
#     print(type(query))
#     response = query_engine.query(query)
#     st.write(response)