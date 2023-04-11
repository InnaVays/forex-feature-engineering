import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []

for page in range(1,3275):
    url = f'https://www.reuters.com/news/archive/marketsNews?view=page&page={page}&pageSize=10'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # find all the cards on the page
    news_cards = soup.find_all('div', class_='story-content')
    # loop through each news card 
    for card in news_cards:
        # get the title and date of the news article
        title = card.find(class_="story-title")
        if title != None :
            title = title.text.strip()
        date = card.find('span', class_='timestamp')
        if date != None :
            date = date.text.strip()
        # store short abstract
        article_short = card.find('p')
        if article_short != None :
            article_short = article_short.text.strip()
        # store the URL
        article_url = card.find('a')['href']
        # append the scraped data to the list
        data.append({'title': title, 'date': date, 'text': article_short, 'href': article_url})

df = pd.DataFrame(data)
df.to_csv('reuters_archive.csv', index=False)