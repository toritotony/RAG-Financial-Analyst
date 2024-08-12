import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, PodSpec
from dotenv import load_dotenv
from bs4 import BeautifulSoup as BS
import requests as rq
from langchain.docstore.document import Document


# Load environment variables
load_dotenv("C:\\Users\\wolfe\\OneDrive\\Desktop\\stock-analyst-tool-llamaindex\\config.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")

headers = {'User-Agent': 'Mozilla/5.0'}
file_path = 'C:\\Users\\wolfe\\OneDrive\\Desktop\\stock-analyst-tool-llamaindex\\articles\\articlelinks.txt'

# Read URLs from file
with open(file_path, 'r', encoding='utf-8') as file:
    urls = [line.strip() for line in file if line.strip()]

print(urls)

# Fetch articles data
articles_data = []
for url in urls:
    print(f"Fetching URL: {url}")
    try:
        webpage = rq.get(url, headers=headers)
        if webpage.status_code == 200:
            trav = BS(webpage.content, "html.parser")
            headline = trav.find('h1', id="articleTitle").text.strip() if trav.find('h1') else None     

            article_text = trav.find_all('p')

            date_elements = trav.find_all('div', class_='flex flex-row items-center')
            published_date = None
            updated_date = None

            for element in date_elements:
                if 'Published' in element.text:
                    published_date = element.find('span').text.strip()

            if headline and article_text and published_date:
                text_content = [p.get_text(strip=True) for p in article_text]
                articles_data.append({'headline': headline, 'link': url, 'content': text_content, 'date': published_date})
            else:
                print(f"No valid content found at {url}")
        else:
            print(f"Failed to fetch URL: {url}")
    except Exception as e:
        print(f"Error fetching URL: {url}, error: {e}")

if not articles_data:
    print("No articles data fetched. Exiting.")
    exit()
else:
    print("ARTICLES DATA: ",articles_data[0])


# Prepare the documents for embedding
docs = []
for article in articles_data:
    combined_content = article['date'] + "    " + article['headline'] + "    ".join(article['content'])
    docs.append(Document(page_content=combined_content))

print("DOCS: ",docs[0])

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)
doc_splits = text_splitter.split_documents(docs)

print("DOCS SPLITS: ", doc_splits[0])

# Initialize embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", chunk_size=200, openai_api_key=OPENAI_API_KEY)

index_name = "test"

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)

# Check if the index exists, if not, create it
if index_name not in pc.list_indexes().names():
    pc.create_index(name=index_name, metric="cosine", dimension=1536, spec=PodSpec(environment=PINECONE_API_ENV, pod_type="s1.x1"))

# Add to vectorDB
vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
vectorstore.add_documents(documents=doc_splits)

retriever = vectorstore.as_retriever()
print(retriever)

with open(file_path, 'w', encoding='utf-8') as file:    
    pass

print("DONE")

