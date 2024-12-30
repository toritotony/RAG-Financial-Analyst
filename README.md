# RAG Analyst - Asset Comparison & Predictive Report Generator

RAG Analyst is a Python-based application designed to automate the collection and analysis of financial data. It leverages advanced web scraping and machine learning techniques to generate insightful reports. These reports include asset outlooks and comparative analyses, integrating both qualitative and quantitative data sourced from [Investing.com](https://www.investing.com). When certain data is unavailable, the tool adapts to provide the most accurate assessment possible based on existing information.

If you'd simply like to use the public version available, reach out for access, and if you already have access, the link is here [RAG Finance App](https://rag-financial-analyst.streamlit.app)

## Features
- **Automated Data Collection**: Scheduled scripts scrape price changes and financial news articles.
- **Vector Database Integration**: Stores processed data in a vector database for efficient querying and retrieval.
- **Comprehensive Reports**: Combines textual analysis with numerical data for detailed financial insights.
- **Adaptability**: Dynamically adjusts reporting based on data availability for specified time periods.

## Installation

Clone the repository available here [RAG Finance App Repository](https://github.com/toritotony/RAG-Financial-Analyst).

## Usage

1. Run `pip install -r requirements.txt` from the directory where your `requirements.txt` file is located.

2. Ensure the following environment variables are configured in a `config.env` file:
   - `OPENAI_API_KEY`
   - `PINECONE_API_KEY`
   - `PINECONE_API_ENV`
   - `PINECONE_INDEX`

3. Use your Task Scheduler and personalize your `example_scheduledtask.bat` file before automating the pipeline flow:
   - Reinstalls packages and libaries necessary for `webscrape.py` and `vectorstore.py`
   - Collect articles and price changes using the `webscrape.py` script.
   - Process and store data using the `vectorstore.py` script.

4. Run `streamlit run app.py` from your virtual environment. This will output a local URL for you to visit the application. Reports will be generated based on available data and stored in the vector database. Certain reports are available now, with limited data on particular assets and stocks.

## Example Scripts

### Data Collection ('webscrape.py')
```
headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://www.investing.com/news/"
webpage = requests.get(url, headers=headers)
trav = BeautifulSoup(webpage.content, "html.parser")
articles = trav.find_all('article', {'data-test': 'article-item'})
```

### Data Storage ('vectorstore.py')
```
text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0)
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)
vectorstore.add_documents(documents=doc_splits)
```

## Dependencies

- **openai**
- **streamlit**
- **langchain & pinecone**: installed via pip when you install requirements.txt file

## Contributing
Contributions and feedback are welcome! Please open an issue to discuss your proposed changes before submitting a pull request. Ensure that all new code is properly tested and documented.

## License
This project is licensed under the [MIT License](https://opensource.org/license/mit)
