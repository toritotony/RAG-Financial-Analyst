from bs4 import BeautifulSoup as BS
import requests as rq
import json

headers = {'User-Agent': 'Mozilla/5.0'}  
#initialize url, webpage, and parsed html page/s
url = "https://www.investing.com/news/"
webpage = rq.get(url, headers=headers)
trav = BS(webpage.content, "html.parser")
articles = trav.find_all('article', {'class': 'js-article-item'})
articles_data = []

for article in articles:
    headline = article.find('a').text.strip()
    link = 'https://www.investing.com' + article.find('a')['href']
    # Fetch the article page
    article_page = rq.get(link, headers=headers)
    article_content = BS(article_page.content, "html.parser")
    # Assume the main content is within <div class="articlePage"> - adjust selector as needed
    article_text = article_content.find_all('p')
    text_content = [p.get_text(strip=True) for p in article_text]
    # Store article data
    articles_data.append({'headline': headline, 'link': link, 'content': text_content})
    print("article text : ", "\n", text_content, "\n\n")
file_path = 'C:\\Users\\wolfe\\OneDrive\\Desktop\\stock-analyst-tool-llamaindex\\articles\\articles.json'  # Specify the path to your file
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(articles_data, f, ensure_ascii=False, indent=4)



# def query(query_engine):
#     st.title('Financial Analyst')

#     st.header("Financial Reports")

#     report_type = st.selectbox(
#         'What type of report do you want?',
#         ('Stock Outlook', 'Competitor Analysis'))


#     if report_type == 'Stock Outlook':
#         symbol = st.text_input("Stock Symbol")

#         if symbol:
#             with st.spinner(f'Generating report for {symbol}...'):
#                 response = query_engine.query(f"Write a report on the outlook for {symbol} stock for the next 5 years. Be sure to include potential risks and headwinds.")

#                 st.write(response)

#     if report_type == 'Competitor Analysis':
#         symbol1 = st.text_input("Stock Symbol 1")
#         symbol2 = st.text_input("Stock Symbol 2")

#         if symbol1 and symbol2:
#             with st.spinner(f'Generating report for {symbol1} vs. {symbol2}...'):
#                 response = query_engine.query(f"Write a report on the competition between {symbol1} stock and {symbol2} stock.")

#                 st.write(response)