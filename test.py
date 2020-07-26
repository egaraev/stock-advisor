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
import subprocess
now = datetime.datetime.now()
currentdate = now.strftime("%Y/%m/%d")
currentdate="2020/07/24"


symbol='AAPL'
mainsite='https://transcriptdaily.com/?s='



subprocess.check_call('curl https://transcriptdaily.com/?s='+symbol+'>news/news.'+symbol+'', shell=True)



#GET LINKS
f = open("news/news."+symbol+"", "r")
html=f.read()
bs = BeautifulSoup(html , 'html.parser')
links = bs.findAll("div", {"id": "wrap"})
links = bs.findAll("div", {"class": "width-limiter main-content"})
links = bs.findAll("p", {"class": "postmeta"})
links = bs.findAll("section", {"class": "archive"})
links = bs.findAll("div", {"class": "entry"})
#print (links)
links = bs.findAll('a')
urls = [link.get('href') for link in links]
#urls = [url for url in urls if url is not None]
news_urls = [url for url in urls if   '/'+currentdate+'/' in url]
stock_urls=news_urls[:1]
del stock_urls[1::2]
print (stock_urls)


#GET TITLES
bs = BeautifulSoup(html , 'html.parser')
titles = bs.findAll("div", {"id": "wrap"})
titles = bs.findAll("div", {"class": "width-limiter main-content"})
titles = bs.findAll("p", {"class": "postmeta"})
titles = bs.findAll("section", {"class": "archive"})
titles = bs.findAll("div", {"class": "entry"})
stock_titles_summ=[]
for i in range (0, 1):
   stock_titles = str(titles[i].text)
   stock_titles=[str(stock_titles.strip())]
   stock_titles_summ +=stock_titles
stock_titles= str(stock_titles_summ[0])  
print (stock_titles)	





#GET DATES
bs = BeautifulSoup(html , 'html.parser')
dates = bs.findAll("div", {"id": "wrap"})
dates = bs.findAll("div", {"class": "width-limiter main-content"})
dates = bs.findAll("p", {"class": "postmeta"})
dates = bs.findAll("section", {"class": "archive"})
dates = bs.findAll("div", {"class": "entry"})
dates = bs.findAll('a')
urls = [link.get('href') for link in links]
urls = [url for url in urls if url is not None]
dates_urls = [url for url in urls if   '/'+currentdate+'/' in url]
del dates_urls[1::2]
stock_dates_summ=''
for i in range (0, 1):
   dates = dates_urls[i]
   dates = dates[28:]
   dates = dates[:10]
#   dates=[dates]
   stock_dates_summ +=dates
stock_dates= stock_dates_summ
print (stock_dates)




#GET NEWS TEXT
stock_text_summ=[]
for i in range (0, 1):
    news_html = requests.get(news_urls[i]).content	
    news_soup = BeautifulSoup(news_html, 'html.parser')
    paragraphs = [par.text for par in news_soup.find_all('p')]
    paragraphs=[paragraphs[3:]]
#    print (paragraphs)
    stock_text_summ +=paragraphs
stock_text=str(stock_text_summ[0])
print (stock_text)








