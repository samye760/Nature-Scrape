import requests
from bs4 import BeautifulSoup
import re
import string
import os

pages: int = int(input())
kind: str = input()

base: str = 'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page='
add: str = 'https://www.nature.com'

for page in range(1, pages + 1):

    new_dir: str = f'Page_{page}'
    cur_dir: str = os.curdir

    os.mkdir(new_dir)
    os.chdir(new_dir)

    soup = BeautifulSoup(requests.get(f'{base}{page}').content, 'html.parser')
    articles = soup.find_all('span', class_='c-meta__type', text=kind)

    for article in articles:

        link = article.find_parent('article').find('a', attrs={
            'href': re.compile("articles")}).get('href')

        new_req = requests.get(''.join([add, link])).content
        new_soup = BeautifulSoup(new_req, 'html.parser')

        title = new_soup.find('h1', class_='c-article-magazine-title').text.strip()
        title: str = ''.join([char if char not in string.punctuation and char != ' ' else '_'
                              for char in title] + ['.txt'])

        body: str = new_soup.find('div', class_='c-article-body').text

        with open(title, 'w', encoding='UTF-8') as target:
            target.write(body)

    os.chdir('..')

print("Saved all articles.")
