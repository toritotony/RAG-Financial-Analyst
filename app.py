import os
import streamlit as st
import pinecone
from dotenv import load_dotenv
from pinecone import PodSpec
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain_core.stores import InMemoryByteStore

# Load environment variables from config.env
#load_dotenv("C:\\Users\\wolfe\\OneDrive\\Desktop\\stock-analyst-tool-llamaindex\\config.env")

# Access API keys and Pinecone configuration
OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
PINECONE_API_KEY = st.secrets['PINECONE_API_KEY[']
PINECONE_API_ENV = st.secrets['PINECONE_ENVIRONMENT']
PINECONE_INDEX = st.secrets['PINECONE_INDEX']

# Initialize Pinecone instance
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)

# Check if the specified index exists; create if necessary
if PINECONE_INDEX not in pc.list_indexes().names():
    pc.create_index(
        name=PINECONE_INDEX,
        dimension=1536,  # Match the dimension of OpenAI embeddings
        metric="cosine",  # Cosine similarity
        spec=PodSpec(
        environment="us-west1-gcp",
        pod_type="s1.x1"
  )
    )

# Initialize OpenAI embeddings and retrieval model
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectorstore = PineconeVectorStore(index_name=PINECONE_INDEX, embedding=embeddings)
retriever = vectorstore.as_retriever()
llm = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY, max_tokens=6000)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)


st.set_page_config(page_title="LLM x VectorDB powered Financial Analyst", layout="centered")
st.title("📊 LLM x VectorDB powered Financial Analyst")
st.markdown(
    """
    Welcome to the Financial Analyst app! Generate comprehensive financial reports 
    using advanced AI-powered analysis. 
    
    Each day a script runs on my Task Scheduler which scrapes articles from Investing.com and stores it into a Pinecone vector database index. This app uses cosine similarity to retrieve the associated articles with the provided stock symbols and generates a report using LLMs. 
    
    Select a report type and provide the required details below.

    credit to PartTimeLarry from Youtube for the idea, just extending it and making it my own with my newfound knowledge in software development and RAG applications.
    """
)

# Report type selection
report_type = st.radio(
    "Select Report Type:",
    ["Single Stock One Year Outlook", "Single Stock Five Year Outlook", "Competitor Analysis", "Sector Analysis"],
    horizontal=True,
    index=0,
)

# Input fields based on report type
col1, col2 = st.columns(2) if report_type == "Competitor Analysis" else (st.container(), None)
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA):") if "Single Stock" in report_type else None
symbol1 = col1.text_input("Enter Stock Symbol 1 (e.g., AAPL):") if report_type == "Competitor Analysis" else None
symbol2 = col2.text_input("Enter Stock Symbol 2 (e.g., MSFT):") if report_type == "Competitor Analysis" else None
sector = st.text_input("Enter Sector Name (e.g., Technology):") if report_type == "Sector Analysis" else None

# Submit button
if st.button("Generate Report"):
    with st.spinner("Generating your report..."):
        try:
            # Build custom queries and prompts based on report type
            if report_type == "Single Stock One Year Outlook" and symbol:
                query = f"Provide a detailed financial outlook for {symbol} stock over the next year. Include recent market trends, key risks, and opportunities."
            elif report_type == "Single Stock Five Year Outlook" and symbol:
                query = f"Write a comprehensive five-year financial outlook for {symbol} stock from 2023 to 2028. Include key market forces, potential risks, and growth opportunities."
            elif report_type == "Competitor Analysis" and symbol1 and symbol2:
                query = f"Compare the financial performance and news of {symbol1} and {symbol2}. Discuss competitive advantages, market trends, and potential challenges."
            elif report_type == "Sector Analysis" and sector:
                query = f"Analyze the current trends and future outlook for the {sector} sector. Include major players, market dynamics, and key opportunities."
            else:
                st.error("Please provide all required inputs.")
                st.stop()

            # Run the query through the QA chain
            response = qa_chain({"query": query})

            # Display the result
            st.success("Report Generated Successfully!")
            st.subheader("📄 Report")
            st.write(response["result"])

            # Display source documents
            st.subheader("📚 Relevant Documents")
            for i, doc in enumerate(response["source_documents"], 1):
                with st.expander(f"Document {i}"):
                    st.write(doc.page_content)

        except Exception as e:
            st.error(f"Error generating report: {e}")