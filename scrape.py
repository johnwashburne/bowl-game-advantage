from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

source = urllib.request.urlopen('https://www.sports-reference.com/cfb/years/1969-bowls.html').read()
games = pd.read_html(source)[0]

for i in range(1970, 2019):
    source = urllib.request.urlopen('https://www.sports-reference.com/cfb/years/{}-bowls.html'.format(i)).read()
    df = pd.read_html(source)[0]
    print(df.head())
    games = games.append(df, ignore_index=True, sort=True)

games.to_csv("games2.csv")
