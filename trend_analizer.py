# Import libraries
import time
import re
import pymysql
import pandas as pd
import sys
import os
import time
import datetime


db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()

def main():
    print('Starting trend analize  module')


    TA()

	
	
def TA():
    for symbol in symbols: #Loop trough the stock summary
        try:
          symbol=(symbol[0])
          name=symbol_full_name(symbol, 3)
          price=hist_price(symbol)
          print (symbol)
          print (price) 
 #         try:
 #             db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
 #             cursor = db.cursor()
 #             cursor.execute("update symbols set advise='%s'  where symbol='%s'" % (postString, symbol))		  
 #             db.commit()
 #         except pymysql.Error as e:
 #             print ("Error %d: %s" % (e.args[0], e.args[1]))
 #             sys.exit(1)
 #         finally:
 #             db.close()



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


def hist_price(symbolname):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    symbol = symbolname
    cursor.execute("SELECT price FROM history WHERE symbol = '%s' order by date desc limit 1" % symbol)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0

if __name__ == "__main__":
    main()
