import os
import gradio as gr
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY') or 'your_default_api_key'

path = "data"

def load_index():
    if not os.path.exists("./storage"):
        # Load the documents and create the index
        documents = SimpleDirectoryReader(path).load_data()
        index = VectorStoreIndex.from_documents(documents)
        # Store it for later
        index.storage_context.persist()
    else:
        # Load the existing index
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)
    return index

index = load_index()
chat_engine = index.as_chat_engine(chat_mode="context", verbose=True, system_prompt=("If you need additional information, ask for it"))

def chat_with_bot(user_input):
    response = chat_engine.chat(user_input)
    return response.response

interface = gr.Interface(
    fn=chat_with_bot,
    inputs=gr.Textbox(lines=2, placeholder="أدخل سؤالك هنا"),
    outputs="text",
    title='المساعد الذكي للقطب الرقمي',
    description='''
    ## معلومات عنا
    هذا التطبيق هو تواصل مع المساعد الذكي للقطب الرقمي.\n \n  تم بناؤه باستخدام
    - Gradio
    - [OpenAI](https://platform.openai.com/docs/models) LLM Model
    - [Pôle Digital](https://www.poledigital.ma/)
    \nتم إنشاؤه من قبل فريق الذكاء الاصطناعي للقطب الرقمي
    ''',
    theme="default",
    examples=[["سؤال عن المساعدات المالية"]]
)

interface.launch(share=True)