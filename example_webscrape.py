from bs4 import BeautifulSoup as BS
import time
import requests as rq
import re

headers = {'User-Agent': 'Mozilla/5.0'}  
url = "https://www.investing.com"
webpage = rq.get(url, headers=headers)
trav = BS(webpage.content, "html.parser")
articles = trav.find_all('div', {'data-test': re.compile('homepage-news-list-item')})
articles_data = [] 

for article in articles:
    a_tag = article.find('a')
    if a_tag is None:
        print("No anchor tag found, skipping...")
        continue
    headline = a_tag.text.strip()
    link = a_tag['href']
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

time.sleep(5)
