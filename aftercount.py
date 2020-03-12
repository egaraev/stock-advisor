import yfinance as yf
import pymysql
import pandas as pd
from yahoo_fin import stock_info as si
import datetime
import time
now = datetime.datetime.now()
currtime = int(time.time())
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols")
symbols=cursor.fetchall()

def main():
    print('Starting stock loop  module')


    SL()


def SL():
    for symbol in symbols: #Loop trough the stock summary
        try:
          market=(symbol[0])
          print (market)
          last= float("{0:.4f}".format(si.get_live_price(market)))  
          #HOW MUCH TO BUY
          bought_price_sql = float(status_orders(market, 3))
          aftercount=float(status_orders(market, 25))
          min_percent=float(status_orders(market, 24))
          aftercount_min=float(status_orders(market, 26))
          order_id = closed_orders_id(market)
          procent_serf = float("{0:.2f}".format(((last / bought_price_sql) - 1) * 100))
          print ("Global buy parameters configured, moving to market loop")
          print (aftercount,  aftercount_min, order_id, procent_serf, min_percent )

          if order_id!=0 and currtime - close_date(market)<432000:

                    try:
                        db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                        cursor = db.cursor()

                        if procent_serf>=percent_serf(market) and procent_serf>=aftercount:
                            cursor.execute(
                                "update orders set aftercount=%s where market = %s and active = 0 and order_id = %s",(procent_serf, market, order_id))
                        elif procent_serf<percent_serf(market) and procent_serf<aftercount_min:
                            cursor.execute(
                                "update orders set aftercount_min=%s where market = %s and active = 0 and order_id = %s",(procent_serf, market, order_id))

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



	
#Check active orders in mysql
	

def status_orders(marketname, value):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 0 and market = '%s' order by order_id desc" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0

	
def close_date(marketname):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT sell_time FROM orders WHERE active=0 and market= '%s' order by order_id desc" % market)
    r = cursor.fetchall()
    for row in r:
        return int(row[0])
    return 0	
	

	
def closed_orders_id(marketname):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT order_id FROM orders where active=0 and market= '%s' order by order_id desc" % market)
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return row[0]

    return 0	
	
	
def percent_serf(marketname):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0






if __name__ == "__main__":
    main()
