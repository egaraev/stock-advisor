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
          db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
          cursor = db.cursor()
          cursor.execute("SELECT price FROM history WHERE symbol = '%s' and price !='None' order by id desc limit 5" % symbol)
          price=cursor.fetchall()
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


def hist_price(symbolname):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    symbol = symbolname
    cursor.execute("SELECT price FROM history WHERE symbol = '%s' order by date desc limit 5" % symbol)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0

if __name__ == "__main__":
    main()
