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
###
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()
###
mainsite='http://www.nasdaq.com'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
headers = {'User-Agent': user_agent}

def main():
    print('Starting nasdaq-news module')

    nasdaq_news()


def nasdaq_news():
    for symbol in symbols: #Loop trough the stock summary
        try:
          symbol=(symbol[0])
          name=symbol_full_name(symbol, 3)
          stock=(symbol+'|'+name)
          print (symbol)
#          print (stock)
          stock_news_urls  = scrape_all_articles(symbol, 1)
#          print (stock_news_urls)
          all_news_urls = list(stock_news_urls)
          all_news_urls = all_news_urls[:5]
#          print (all_news_urls)
          all_titles = [scrape_news_title(news_url) for news_url in all_news_urls]
#          all_stock_titles = all_titles
          all_stock_titles = [re.search(stock, w) for w in all_titles]
          title_indices = [all_stock_titles.index(w) for w in all_stock_titles if w is not None]
          stock_titles = [all_titles[w] for w in title_indices]
          stock_urls = [all_news_urls[w] for w in title_indices]
          stock_dates = [scrape_news_date(mainsite+news_url) for news_url in stock_urls]
          stock_articles = [scrape_news_text(mainsite+news_url) for news_url in stock_urls]
          print (stock_dates, stock_titles)


           ## save it for further use
          stock_articles = pd.DataFrame(stock_articles)
          stock_titles = pd.DataFrame(stock_titles)
          stock_dates = pd.DataFrame(stock_dates)
          stock_urls = pd.DataFrame(stock_urls)

          # Export data to csv
#          stock_articles.to_csv(f'csvs/{symbol}_articles.csv', index = None, header=True)
#          stock_titles.to_csv(f'csvs/{symbol}_titles.csv', index = None, header=True)
#          stock_dates.to_csv(f'csvs/{symbol}_dates.csv', index = None, header=True)
#          stock_urls.to_csv(f'csvs/{symbol}_urls.csv', index = None, header=True)


          # Import data back

#          stock_articles = pd.read_csv(r"csvs/{symbol}_articles.csv") 
#          stock_titles = pd.read_csv(r'csvs/{symbol}_titles.csv')
#          stock_dates = pd.read_csv(r'csvs/{symbol}_dates.csv')


          stock_titles.columns = ['stock_titles']
          stock_titles = stock_titles['stock_titles'].tolist()
          stock_articles.columns = ['stock_articles']
          stock_articles = stock_articles['stock_articles'].tolist()




          stock_dates.columns = ['stock_dates']
          stock_dates = stock_dates['stock_dates'].tolist()
          stock_urls.columns = ['stock_urls']
          stock_urls = stock_urls['stock_urls'].tolist()



          open("csvs/tmp-sql.txt", "w").close()
          for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
             if i != "":
#                 print (stock_dates[i]) 
               if stock_dates[i] != None:
                 f = open("/root/PycharmProjects/stock-advisor/csvs/tmp-sql.txt", "a")
                 print(stock_titles[i], file=f)
#                print ('\n', file=f)
                 print(stock_dates[i], file=f)
#                print ('\n', file=f)
                 print(stock_articles[i][:-3110], file=f)
#                 print(stock_articles[i][:1000], file=f)
                 print('<a href="'+mainsite+stock_urls[i]+'">'+mainsite+stock_urls[i]+'</a>', file=f)
                 print ('\n', file=f)
                 f.close()
             f = open("/root/PycharmProjects/stock-advisor/csvs/tmp-sql.txt", "r", newline="\n")
             news= (f.read())
             try:
                 db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                 cursor = db.cursor()
                 cursor.execute('update symbols set news = %s where symbol=%s',(news, symbol))
                 db.commit()
             except pymysql.Error as e:
                 print ("Error %d: %s" % (e.args[0], e.args[1]))
                 sys.exit(1)
             finally:
                 db.close()

             f.close()
#             time.sleep(60)




        except:
            continue








## for extracting news date
def scrape_news_date(news_url):
    try:
#        news_html = urlopen(news_url)
        date_now = time.strftime("%A, %d/%m/%Y - %H:%M")
        newdate = datetime.datetime.strptime(date_now, "%A, %d/%m/%Y - %H:%M")
        currentdate = newdate.date().strftime("%Y-%m")

        url = (news_url)
        news_html = requests.get(url, headers=headers).content
        news_soup = BeautifulSoup(news_html , 'html.parser')
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

        stringdate=datetime.datetime.strptime(news_date, "%a, %m/%d/%Y - %H:%M")
        newstringdate= stringdate.date().strftime("%Y-%m")
        if currentdate == newstringdate:
           return news_date

#        return news_date
    except:
        return '0'

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
    website = 'http://www.nasdaq.com/market-activity/stocks/' + ticker + '/news-headlines'
    all_news_urls = get_news_urls(website)

    ind = 2
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

