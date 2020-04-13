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
from urllib.request import urlopen
import time
import datetime
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
currentdate = now.strftime("%Y-%m-%d")
import numpy as np
import statistics

import nltk
import warnings
warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()



###
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT * FROM symbols WHERE active=1")
symbols=cursor.fetchall()
###
mainsite='https://old.nasdaq.com'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
headers = {'User-Agent': user_agent}

def main():
    print('Starting nasdaq-news score module')

    nasdaq_news()


def nasdaq_news():
    for symbol in symbols: #Loop trough the stock summary
        try:
          symbol=(symbol[1])
          symbol_id=(symbol[0])
          name=symbol_full_name(symbol, 3)
#          stock=(symbol+'|'+name)
          print (symbol)
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
		  
		  
          url = (mainsite+'/symbol/'+symbol)
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
             news_html = requests.get(newurl).content
             news_soup = BeautifulSoup(news_html, 'html.parser')
             result = news_soup.findAll("div", {"id": "articleText"})
             result= news_soup.select('p')
             for script in news_soup(["script", "style", "img", "div", "p"]): # remove all javascript and stylesheet code
                script.extract()    
             news_text1=str(result[0])
             news_text2=str(news_text1[3:])
             stock_articles=news_text2.strip()[:-4]	
    
          else:
             print ("Request was not redirected")
             news_html = requests.get(stock_urls).content	
             news_soup = BeautifulSoup(news_html, 'html.parser')
             paragraphs = [par.text for par in news_soup.find_all('p')]
             stock_articles = ' '.join(paragraphs[1:-4]) 
          print (stock_articles )


          open("csvs/tmp-score.txt", "w").close()
          passage=(stock_articles)
          f1 = open("/root/PycharmProjects/stock-advisor/csvs/tmp-score.txt", "a")
          print (round(sia.polarity_scores(passage)['compound'], 2), file=f1)
          f1.close()
          f1 = open("/root/PycharmProjects/stock-advisor/csvs/tmp-score.txt", "r", newline="\n")
          scores= (f1.readlines())


          f1.close()

          scores2 = [x.replace('\n', '') for x in scores]
          lenght= (len(scores2))
          new_list =sum(float(t) for t in scores2)
          average=new_list/lenght
#             print (new_list)
#             minimal_score=(min(scores))
          print (average)

             
          try:
                 db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                 cursor = db.cursor()
                 cursor.execute("update history set news_score='%s'  where symbol='%s' and date='%s'" % (average, symbol, currentdate))
                 cursor.execute("update symbols set news_score='%s'  where symbol='%s'" % (average, symbol))
                 db.commit()
          except pymysql.Error as e:
                 print ("Error %d: %s" % (e.args[0], e.args[1]))
                 sys.exit(1)
          finally:
                 db.close()
				 
#             time.sleep(60)


        except:
            continue




## for extracting news date
def scrape_news_date(news_url):
    try:
#        news_html = urlopen(news_url)
#        date_now = time.strftime("%A, %d/%m/%Y - %H:%M")
#        newdate = datetime.datetime.strptime(date_now, "%A, %d/%m/%Y - %H:%M")
#        currentdate = newdate.date().strftime("%Y-%m")

        url = (news_url)
        news_html = requests.get(url, headers=headers).content
        news_soup = BeautifulSoup(news_html , 'html.parser')
        result = news_soup.findAll("div", {"class": "news-headlines"})
        result=news_soup.select('small')
        result=(news_soup.find(text=re.compile('Reuters')))
        news_date = result.strip()[:-13]
#        jsonresult=(news_soup.findAll('script', {'type':'application/ld+json'}))
        # Convert show_data to string
#        show_data = str( jsonresult )
        # Find last character of opening script tag
#        first = show_data.find( '>' )
        # Find first character of closing script tag
#        last = show_data.rfind( '<' )
        # Get whatever is between the indeces
#        show_data = show_data[first+1:last]
        # Loads show_data string into dictionary
#        jsondict = json.loads( show_data )
#        news_date = (jsondict['@graph'][2]['datePublished'])

#        stringdate=datetime.datetime.strptime(news_date, "%a, %m/%d/%Y - %H:%M")
#        newstringdate= stringdate.date().strftime("%Y-%m")
#        if currentdate == newstringdate:
        return news_date


    except:
        return '0'

## for extracting news title
def scrape_news_title(news_url):
    news_html = requests.get(mainsite+news_url).content
    news_soup = BeautifulSoup(news_html , 'html.parser')
#    news_title = news_soup.title.text
    results = news_soup.findAll("div", {"class": "news-headlines"})
    result = news_soup.find_all('a', target="_self")
    news_title = result[1].text
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

def scrape_all_info(all_news_urls):
    all_news_urls = list(set(all_news_urls))
    all_articles = [scrape_news_text(news_url) for news_url in all_news_urls]
    all_titles = [scrape_news_title(news_url) for news_url in all_news_urls]
    all_dates = [scrape_news_date(news_url) for news_url in all_news_urls]
    return all_articles, all_titles, all_dates


def symbol_full_name(symbolname, value):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    symbol = symbolname
    cursor.execute("SELECT * FROM symbols WHERE symbol = '%s'" % symbol)
    r = cursor.fetchall()
    for row in r:
        if row[1] == symbolname:
            return row[value]

    return False




if __name__ == "__main__":
    main()

