from  bs4 import BeautifulSoup
import os
import re
import requests
import time
from urllib.request import urlretrieve

def myfilter(tag):
    def tryparent(tag):
        try:
            return re.match('[A-Z]', tag.parent.parent.previous_sibling.previous_sibling.span.text)
        except:
            False
    return tag and tag.name == 'a' and tag.parent.name == 'li' and tag.get('href').startswith('/wiki/') and not tag.previous_sibling and tryparent(tag)

def get_links(soup):
    return [l.get('href') for l in soup.find_all(myfilter)]

soup = BeautifulSoup(requests.get('https://en.wikipedia.org/wiki/List_of_computer_scientists').text, "html.parser")

links = get_links(soup)
print('found %d links' % len(links))

os.makedirs('data', exist_ok=True)
for link in links[0:300]:
    url = 'https://en.wikipedia.org' + link
    page = requests.get(url) 
    soup = BeautifulSoup(page.content, 'html.parser') 
    text = ""
    for paragraph in soup.find_all('p'):
        text += paragraph.text
    text = re.sub(r'[0-9]+', ' ', text)
    text = re.sub(r'\[\d+\]', ' ', text.strip())
    text = re.sub(r'[^\w\s]',' ',text)

    text = re.sub('(\s+)(a|an|and|the|plus|also|as|when|while)(\s+)', ' ', text).lower()
    text = re.sub('(\s+)(then|after|a|but|by|this)(\s+)', ' ', text)
    text = re.sub('(\s+)(so|at|to|of|is|are|on|in|for)(\s+)', ' ', text)
    
    file = open("./data/"+link[6:]+".txt", "w")
    file.write(str(text))
    file.close()
