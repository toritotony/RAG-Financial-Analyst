from bs4 import BeautifulSoup as BS
import requests as rq

headers = {'User-Agent': 'Mozilla/5.0'}  
url = "https://www.investing.com/news/"
webpage = rq.get(url, headers=headers)
trav = BS(webpage.content, "html.parser")
articles = trav.find_all('article', {'data-test': 'article-item'})
articles_data = []

for article in articles:
    headline = article.find('a', {'data-test': 'article-title-link'}).text.strip()
    link = article.find('a', {'data-test': 'article-title-link'})['href']
    full_link = 'https://www.investing.com' + link if not link.startswith('http') else link
    # Fetch the article page
    article_page = rq.get(full_link, headers=headers)
    article_content = BS(article_page.content, "html.parser")
    article_text = article_content.find_all('p')
    text_content = [p.get_text(strip=True) for p in article_text]
    # Store article data
    articles_data.append({'headline': headline, 'link': full_link, 'content': text_content})

file_path = 'path to where your articles.txt will be located locally'

with open(file_path, 'a', encoding='utf-8') as f:
    for article in articles_data:
       f.write(article['link'] + '\n')
