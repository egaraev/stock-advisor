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
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
currentdate = now.strftime("%Y-%m-%d")

db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()

def main():
    print('Starting marketwatch  module')


    SL()

	
	
def SL():
    for symbol in symbols: #Loop trough the stock summary
        try:
          symbol=(symbol[0])
          name=symbol_full_name(symbol, 3)
          print (symbol)
          url = ('https://www.marketwatch.com/investing/stock/' + symbol + '/analystestimates')
          response = requests.get(url)
          soup = BeautifulSoup(response.text, "html.parser")
          divs = soup.findAll("table", {"class": "ratings"})
          result=soup.findAll('tr', class_='last')
          title_list =[]
          for item in result: 
             individualtitle = item.get_text() 
             title_list.append(individualtitle)
          listToStr = '\n'.join([str(elem) for elem in title_list]) 
          list=listToStr.rsplit("\n", 3)[0]
          removelast=(list[5:])
          postString = (removelast.split("\n",2)[1])		  
          #print(postString)
          printed = (name, postString)
          try:
              db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
              cursor = db.cursor()
              cursor.execute("update symbols set advise='%s'  where symbol='%s'" % (postString, symbol))
              cursor.execute("update history set advise='%s' where symbol='%s' and date='%s'" % (postString, symbol, currentdate))
              cursor.execute('insert into logs(date, entry) values("%s", "%s")', (currenttime, printed))			  
              db.commit()
          except pymysql.Error as e:
              print ("Error %d: %s" % (e.args[0], e.args[1]))
              sys.exit(1)
          finally:
              db.close()



        except:
            continue

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


