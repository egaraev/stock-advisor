import pymysql
import pandas as pd
import time
import datetime
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d")
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()


def main():
    print('Starting stock loop  module')


    SL()


def SL():
    for symbol in symbols: #Loop trough the stock summary
        try:
          symbol=(symbol[0])
          print (date_exist(symbol, currenttime))
#          print (symbol, currenttime)
          if date_exist(symbol, currenttime) != 1:
             try:
                 db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                 cursor = db.cursor()
                 cursor.execute('insert into history(date, symbol) values(%s, %s)', (currenttime, symbol))
                 db.commit()
             except pymysql.Error as e:
                 print ("Error %d: %s" % (e.args[0], e.args[1]))
                 sys.exit(1)
             finally:
                 db.close()
          else:
              pass

          	  
			  

        except:
            continue


			
			
			
			
			
def date_exist(symbolname, currenttime):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    symbol = symbolname
    cursor.execute("SELECT * FROM history WHERE symbol = '%s' and date='%s'" % (symbol, currenttime))
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return 1

        else:
            return 0


if __name__ == "__main__":
    main()
