import sys
import os
import re
import pymysql
import pandas as pd
import yfinance as yf
from yahoo_fin import stock_info as si
from dateutil import parser
import requests
from bs4 import BeautifulSoup
import json
import urllib
from urllib.request import urlopen
import time

###
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()


def main():
    print('Starting nasdaq-sentiment module')

    nasdaq_sentiments()




def nasdaq_sentiments():
    for symbol in symbols: #Loop trough the stock summary
        try:
          symbol=(symbol[0])
          print (symbol)
          stock = yf.Ticker(symbol)
          print (si.get_live_price(symbol))

#          print (si.get_quote_table(symbol , dict_result = True))
          hist = stock.history(period="1d")
          df = pd.DataFrame(hist)
          print (df['Open'].tolist())
          print (df['Close'].tolist())
          print (df['Low'].tolist())
          print (df['High'].tolist())



          


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



