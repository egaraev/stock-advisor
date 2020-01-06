## First, here specific web scraping functions are defined

from dateutil import parser
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import json
import urllib
from urllib.request import urlopen



dow_info = pd.read_html('https://finance.yahoo.com/quote/%5EDJI/components?p=%5EDJI')[0]
dow_tickers = dow_info.Symbol.tolist()
mainsite='http://www.nasdaq.com'


## for extracting news date
def scrape_news_date(news_url):
    try:        
#        news_html = requests.get(mainsite+news_url).content
        news_html = urlopen(news_url) 
        news_soup = BeautifulSoup(news_html , 'html.parser')
#        all_p = news_soup.find('span', {'itemprop':'datePublished'})
#        news_date = all_p.text
#        news_date = parser.parse(news_date)

        jsonresult=(news_soup.findAll('script', {'type':'application/ld+json'}))
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
        news_date = (jsondict['@graph'][2]['datePublished'])
#        news_date = parser.parse(news_date)

        return news_date
    except:
        return 'No date'

## for extracting news title
def scrape_news_title(news_url):
    news_html = requests.get(mainsite+news_url).content 
    news_soup = BeautifulSoup(news_html , 'html.parser')
    news_title = news_soup.title.text
    return news_title

## for extracting news text
def scrape_news_text(news_url):
    news_html = requests.get(news_url).content
    news_soup = BeautifulSoup(news_html , 'html.parser') 
    paragraphs = [par.text for par in news_soup.find_all('p')]
    news_text = ' '.join(paragraphs[1:-4]) ## just for the Nasdaq.com case
    return news_text

def get_news_urls(links_site):
    resp = requests.get(links_site)
    if not resp.ok:
        return None
 
    html = resp.content
    bs = BeautifulSoup(html , 'html.parser') 
    links = bs.find_all('a')

    urls = [link.get('href') for link in links]
    urls = [url for url in urls if url is not None] 
    news_urls = [url for url in urls if '/articles/' in url]
 
    return news_urls

def scrape_all_articles(ticker , page_limit):
    website = 'http://www.nasdaq.com/symbol/' + ticker + '/news-headlines'
    all_news_urls = get_news_urls(website)
    
    ind = 2
    while ind <= page_limit:
        current_site = website + '?page=' + str(ind)
        urls_list = get_news_urls(current_site)
        
        all_news_urls = all_news_urls + urls_list
        ind += 1
    return all_news_urls
 
def scape_all_info(all_news_urls):
    all_news_urls = list(set(all_news_urls))
    all_articles = [scrape_news_text(news_url) for news_url in all_news_urls]
    all_titles = [scrape_news_title(news_url) for news_url in all_news_urls]
    all_dates = [scrape_news_date(news_url) for news_url in all_news_urls]
    return all_articles, all_titles, all_dates


##################
ap_news_urls  = scrape_all_articles('aapl' , 100)
#print (dow_tickers)

all_news_urls = list(set(ap_news_urls))
#print (len(all_news_urls))


all_titles = [scrape_news_title(news_url) for news_url in all_news_urls]
all_apple_titles = [re.search("Apple", w) for w in all_titles]

title_indices = [all_apple_titles.index(w) for w in all_apple_titles if w is not None]
apple_titles = [all_titles[w] for w in title_indices]

#print (len(apple_titles))


apple_urls = [all_news_urls[w] for w in title_indices] 
apple_dates = [scrape_news_date(mainsite+news_url)  for news_url in apple_urls]    
apple_articles = [scrape_news_text(mainsite+news_url) for news_url in apple_urls]

## save it for further use
apple_articles = pd.DataFrame(apple_articles)
apple_titles = pd.DataFrame(apple_titles)
apple_dates = pd.DataFrame(apple_dates)
apple_urls = pd.DataFrame(apple_urls)



#print (apple_urls)
#print (apple_dates)
#print (apple_titles)
#print (apple_articles)


apple_articles.to_csv(r'csvs/apple_articles.csv', index = None, header=True)
apple_titles.to_csv(r'csvs/apple_titles.csv', index = None, header=True)
apple_dates.to_csv(r'csvs/apple_dates.csv', index = None, header=True)
apple_urls.to_csv(r'csvs/apple_urls.csv', index = None, header=True)


# Import data back

apple_articles = pd.read_csv(r"csvs/apple_articles.csv") 
apple_titles = pd.read_csv(r'csvs/apple_titles.csv')
apple_dates = pd.read_csv(r'csvs/apple_dates.csv')

apple_articles.columns = ['apple_articles']
apple_articles = apple_articles['apple_articles'].tolist()

apple_dates.columns = ['apple_dates']
apple_dates = apple_dates['apple_dates'].tolist()


print (apple_dates)
print (apple_articles)





