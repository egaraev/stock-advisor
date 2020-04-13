# Import libraries
import requests
import urllib.request
import time
import re
from bs4 import BeautifulSoup
import pymysql
import pandas as pd
import sys
import os
import time
import datetime
import sys
import os
import re
import pymysql
import pandas as pd
from dateutil import parser
import requests
from bs4 import BeautifulSoup
import json
import urllib
import urllib.request
from urllib.request import urlopen
import time
import datetime
symbol='cci'
mainsite='https://old.nasdaq.com'

def get_news_urls(links_site):
    resp = requests.get(links_site)
    if not resp.ok:
        return None

    html = resp.content
    bs = BeautifulSoup(html , 'html.parser')
    links = bs.find_all('a')

    urls = [link.get('href') for link in links]
    urls = [url for url in urls if url is not None]
    news_urls = [url for url in urls if '/article/' in url]

    return news_urls

	
def scrape_all_articles(ticker , page_limit):
    website = 'https://old.nasdaq.com/symbol/' + ticker
    all_news_urls = get_news_urls(website)

    ind = 1
    while ind <= page_limit:
        current_site = website + '?page=' + str(ind)
        urls_list = get_news_urls(current_site)

        all_news_urls = all_news_urls + urls_list
        ind += 1
    return all_news_urls	


	
def cleanMe(html):
    soup = BeautifulSoup(html, "html.parser") # create a new bs4 object from the html data loaded
#    soup = soup.findAll("div", {"id": "articleText"})
    for script in soup(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text	
	
	
stock_news_urls  = scrape_all_articles(symbol, 1)
all_news_urls = list(stock_news_urls)
all_news_urls = all_news_urls[:1]
stock_urls=str(all_news_urls[0])
print (stock_urls)
	
news_html = requests.get(mainsite+'/symbol/'+symbol).content
news_soup = BeautifulSoup(news_html , 'html.parser')
results = news_soup.findAll("div", {"class": "news-headlines"})
result = news_soup.find_all('a', target="_self")
stock_titles = str(result[1].text)
stock_titles=str(stock_titles.strip())		  
print (stock_titles)	

url = ('https://old.nasdaq.com/symbol/cci')
news_html = requests.get(url)
news_soup = BeautifulSoup(news_html.text , 'html.parser')
results = news_soup.findAll("div", {"id": "CompanyNewsCommentary"})
result = news_soup.find("ul", {"class": "orange-ordered-list"})
result= news_soup.select('small')
result=str(result[1])
stock_dates = str(result.strip()[7:])
stock_dates = stock_dates.strip()[:-20]	
print (stock_dates)




response = requests.get(stock_urls)
if response.history:
    print ("Request was redirected")
    for resp in response.history:
        print (resp.status_code, resp.url)
    print ("Final destination:")
    print (response.status_code, response.url)
    newurl=response.url
#    print (newurl)
    news_html = requests.get(newurl).content
    news_soup = BeautifulSoup(news_html, 'html.parser')
    result = news_soup.findAll("div", {"id": "articleText"})
    result= news_soup.select('p')
    for script in news_soup(["script", "style", "img", "div", "p"]): # remove all javascript and stylesheet code
        script.extract()    
    news_text1=str(result[0])
    news_text2=str(news_text1[3:])
    news_text=news_text2.strip()[:-4]	
    
else:
    print ("Request was not redirected")
    news_html = requests.get(stock_urls).content	
    news_soup = BeautifulSoup(news_html, 'html.parser')
    paragraphs = [par.text for par in news_soup.find_all('p')]
    news_text = ' '.join(paragraphs[1:-4]) 	
print (news_text)





