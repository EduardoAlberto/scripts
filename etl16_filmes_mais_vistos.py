# ranking dos filmes mais votados imdb
import requests
import pandas as pd
from bs4 import BeautifulSoup



url = "https://www.imdb.com/search/title/?groups=top_100&sort=user_rating,desc"
table = []
response = requests.get(url)
if response.status_code == 200:
    html = response.content
    soup = BeautifulSoup(html, 'lxml')
    for rn in soup.find_all("h3",{"class":"lister-item-header"}):
        txt = rn.text.strip().replace("\n",'')
        table.append(txt)
    tx = pd.DataFrame(table)
    print(tx)


