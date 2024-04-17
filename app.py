import os, config, json
from llama_index.core import Settings, VectorStoreIndex, StorageContext, load_index_from_storage
os.environ['OPENAI_API_KEY'] = config.OPENAI_API_KEY

import streamlit as st
from llama_index.core import ServiceContext
from langchain.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

Settings.llm = OpenAI(model_name='gpt-4', max_tokens=6000)
Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-small')
service_context = ServiceContext.from_defaults(llm=Settings.llm)

# Load the index from a JSON file (you must define this function)
def load_index_from_json(file_path, service_context):
    with open(file_path, 'r') as file:
        data = json.load(file)
    index = VectorStoreIndex(data, service_context)
    return index

# Replace load_from_disk with the new JSON loading approach
index = load_index_from_json('index_news.json', service_context=service_context)

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine(llm=Settings.llm)

st.title('Financial Analyst')

st.header("Financial Reports")

report_type = st.selectbox(
    'What type of report do you want?',
    ('Single Stock Outlook', 'Competitor Analysis'))


if report_type == 'Single Stock Outlook':
    symbol = st.text_input("Stock Symbol")

    if symbol:
        with st.spinner(f'Generating report for {symbol}...'):
            response = query_engine.query(f"Write a report on the outlook for {symbol} stock from the years 2023-2027. Be sure to include potential risks and headwinds.")

            st.write(response)

if report_type == 'Competitor Analysis':
    symbol1 = st.text_input("Stock Symbol 1")
    symbol2 = st.text_input("Stock Symbol 2")

    if symbol1 and symbol2:
        with st.spinner(f'Generating report for {symbol1} vs. {symbol2}...'):
            response = query_engine.query(f"Write a report on the competition between {symbol1} stock and {symbol2} stock.")

            st.write(response)




