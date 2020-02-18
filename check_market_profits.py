import yfinance as yf
import pymysql
import pandas as pd
import os
from yahoo_fin import stock_info as si
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()

def main():
    print('Starting market profits checking module')


    SUMM()


def SUMM():
    open('data/out2_tmp.csv', 'w').close()
    open('data/out3_tmp.csv', 'w').close()
    open('data/out4_tmp.csv', 'w').close()
    for symbol in symbols: #Loop trough the stock summary
          market=(symbol[0])
          #print (symbol)
          #market = yf.Ticker(symbol)
          print (market, summ_serf(market))
          if summ_serf(market)!=0:
              #print (market, summ_serf(market), count(market))
              f= open('data/out2_tmp.csv', 'a')
              print (str(market), file=f)
              f1=open('data/out3_tmp.csv', 'a')
              print (summ_serf(market), file=f1)
              f2 = open('data/out4_tmp.csv', 'a')
              print (count(market), file=f2)
    os.rename('data/out2_tmp.csv', 'data/out2.csv')
    os.rename('data/out3_tmp.csv', 'data/out3.csv')
    os.rename('data/out4_tmp.csv', 'data/out4.csv')

def summ_serf(marketname):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT SUM(percent_serf) FROM orders where active=0 and market= '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

    return 0




def count(marketname):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT COUNT(*) FROM orders where active=0 and market= '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

    return 0


if __name__ == "__main__":
    main()
