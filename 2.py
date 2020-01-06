import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
headers = {'User-Agent': user_agent}

#html = urlopen("https://www.nasdaq.com/articles/nasdaq-positive-for-the-week-despite-airstrike-concerns-2020-01-06")
url = 'https://www.nasdaq.com/articles/nasdaq-positive-for-the-week-despite-airstrike-concerns-2020-01-06'
html = requests.get(url, headers=headers).content

#soup = BeautifulSoup(html.read(), features="lxml");
soup = BeautifulSoup(html , 'html.parser')


jsonresult=(soup.findAll('script', {'type':'application/ld+json'}))
#print (jsonresult)


# Convert show_data to string
show_data = str( jsonresult )

# Find last character of opening script tag
first = show_data.find( '>' )

# Find first character of closing script tag
last = show_data.rfind( '<' )

# Get whatever is between the indeces
show_data = show_data[first+1:last]

# Loads show_data string into dictionary    
jsondict = json.loads( show_data )



print (jsondict['@graph'][2]['datePublished'])




#print ([meta.get('content') for meta in soup.find_all('meta', 'datePublished')])
