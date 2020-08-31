import yfinance as yf
import pymysql
import pandas as pd
from yahoo_fin import stock_info as si
import sys
import smtplib
#import calendar
import time
import datetime
import requests
import json
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()


def main():
    print('Starting stock buy  module')


    Buy()

	

def Buy():
    for symbol in symbols: #Loop trough the stock summary
        try:
          market=(symbol[0])
          print (market)
          stock = yf.Ticker(market)
          last= float("{0:.4f}".format(si.get_live_price(market)))
          hist = stock.history(period="1d")
          df = pd.DataFrame(hist)
          #print (df)
          day_close = (df['Close'][0].tolist())
          buy_size = parameters()[0] #The size for opening orders for STOP_LOSS mode
          stop_bot_force = parameters()[4]  #If stop_bot_force==1 we  stop bot and close all orders
          stop_bot = parameters()[10]
          #print (stop_bot_force)
          currtime = int(time.time())
          today = datetime.datetime.now().date()
          debug_mode=parameters()[9]
          max_orders = parameters()[5]
          bot_token= parameters()[11]
          bot_chatID= parameters()[12]
          #print (bot_token, bot_chatID)
          print ("Global buy parameters configured, moving to market loop")
          #dayofweek=weekday()		  
          timestamp = int(time.time())
          #How much market has been changed
          percent_chg = float("{0:.4f}".format(((last / day_close) - 1) * 100))
          #HOW MUCH TO BUY
          buy_quantity = float("{0:.4f}".format(buy_size / last))
          bought_price_sql = float(status_orders(market, 3))
          bought_quantity_sql = float(status_orders(market, 2))
          active = active_orders(market)
          timestamp_old = int(timestamp_orders(market))
          now = datetime.datetime.now()
          currenttime = now.strftime("%Y-%m-%d %H:%M")
          heikin_ashi=market_values(market,5)
          candle_direction=market_values(market,7)
          tweet_positive=market_values(market,8)
          hour_candle_direction=market_values(market,21)
          tweet_negative=market_values(market,9)
          tweet_ratio = float("{0:.4f}".format(tweet_positive/tweet_negative))
          #print (tweet_ratio)
          ai_price=market_values(market,11)
          if ai_price<last:
             ai_direction="DOWN"
          elif ai_price>last:
             ai_direction="UP"
          else:
             ai_direction="NONE"
             
          tweet_polarity=market_values(market,13)
          tweet_score=market_values(market,15)
          candle_score=market_values(market,17)
          news_score=market_values(market,20)
          candle_pattern=market_values(market,18)
          previous_date = market_values(market,22)
          #print (heikin_ashi, candle_direction,tweet_positive,tweet_negative,tweet_polarity,tweet_score,candle_score )
          print (previous_date)
	
	




		  
          print ("Market parameters configured, moving to buy for ", market)		  

          try:
               db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
               cursor = db.cursor()
               serf = float("{0:.4f}".format(last * bought_quantity_sql - bought_price_sql * bought_quantity_sql))
               #print (last,bought_price_sql,bought_quantity_sql )

               if bought_price_sql!=0:
                   procent_serf = float("{0:.2f}".format(((last / bought_price_sql) - 1) * 100))
                   #print (market, procent_serf)

                   if procent_serf>=percent_serf_max(market):
                       cursor.execute("update orders set percent_serf_max=%s where market = %s and active =1 and open_sell=0 ",(procent_serf, market))
                   elif procent_serf<percent_serf_min(market):
                       cursor.execute("update orders set percent_serf_min=%s where market = %s and active =1 and open_sell=0 ",(procent_serf, market))
                   else:
                       cursor.execute("update orders set percent_serf=%s where market = %s and active =1 and open_sell=0 ",(procent_serf, market))
               #print (serf)
               #cursor.execute("update orders set serf = %s where market = %s and active =1" , (serf, market))
               cursor.execute("update orders set serf_usd = %s where market = %s and active =1", (serf, market))	   
               cursor.execute('update symbols set current_price = %s  where symbol = %s and active =1', (last, market))
               db.commit()
               
          except pymysql.Error as e:
               print ("Error %d: %s" % (e.args[0], e.args[1]))
               sys.exit(1)
          finally:
               db.close()


          max_percent_sql = status_orders(market, 15)

          print ("Updated serf and procent serf stuff for", market)


		  
          print ("Starting buying mechanizm for " , market)


          if (stop_bot == 0)  and tweet_positive>tweet_negative and heikin_ashi!="DOWN" and heikin_ashi!="Revers-DOWN" and candle_score>=0 and tweet_polarity>0.14 and news_score>=0.9 and candle_direction=="U" and hour_candle_direction=="U" and today!=previous_date: # and ai_direction=="UP":

              # If we have some currency on the balance
                  if bought_quantity_sql !=0.0:
                      print ('    2 - We already have ' + str(format_float(bought_quantity_sql)) + '  ' + market + ' on our balance')
                      try:
                          printed = ('    2 - We already have ' + str(format_float(bought_quantity_sql)) + '  ' + market + ' on our balance')
                          db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                          cursor = db.cursor()
                          cursor.execute('insert into logs(date, entry) values("%s", "%s")' % (currenttime, printed))
                          db.commit()
                      except pymysql.Error as e:
                          print ("Error %d: %s" % (e.args[0], e.args[1]))
                          sys.exit(1)
                      finally:
                          db.close()
                            # if we have some active orders in sql
                  elif active == 1:
                      print  ('    3 - We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                      try:
                          printed = ('    3 - We already have ' + str(float(status_orders(market, 2))) + ' units of ' + market + ' on our balance')
                          db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                          cursor = db.cursor()
                          cursor.execute('insert into logs(date, entry) values("%s", "%s")' % (currenttime, printed))
                          db.commit()
                      except pymysql.Error as e:
                          print ("Error %d: %s" % (e.args[0], e.args[1]))
                          sys.exit(1)
                      finally:
                          db.close()
                  else:
                        # Buy some currency by market analize first time
                      try:
                          print ('    4- Purchasing '  + str(format_float(buy_quantity)) + ' units of ' + market + ' for ' + str(format_float(last)))
                          printed = ('    I would strongly advise to purchase any amount of ' + market + ' for this current price ' + str(format_float(last))+'. Why? Because now we have great conditions for this: Heikin Ashi indicator is: ' + str(heikin_ashi) + '  Candle_direction: ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) +' Tweet_ratio: ' +str(tweet_ratio) + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score)+ ' Candle_pattern: ' + str(candle_pattern)+ ' News_score: ' + str(news_score)+ ' H_candle_dir: ' + str(hour_candle_direction)+' For more details go here: http://139.162.132.189')
                          db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                          cursor = db.cursor()
                          cursor.execute('insert into logs(date, entry) values("%s", "%s")' % (currenttime, printed))
                          cursor.execute('insert into orders(market, quantity, price, active, date, timestamp, params) values("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (market, buy_quantity, last, "1", currenttime, timestamp,  '  HA: ' + str(heikin_ashi) + '  Candle_direction: ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) + ' Tweet_ratio: ' +str(tweet_ratio) + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score)+ ' Candle_pattern: ' + str(candle_pattern)+ ' News_score: ' + str(news_score)+ ' H_candle_dir: ' + str(hour_candle_direction) ))
                          cursor.execute("update orders set serf = %s where market = %s and active =1",(serf, market))
                          db.commit()
                      except pymysql.Error as e:
                          print ("Error %d: %s" % (e.args[0], e.args[1]))
                          sys.exit(1)
                      finally:
                          db.close()
                      #Mail("egaraev@gmail.com", "egaraev@gmail.com", "New purchase", printed, "localhost")
                      send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + printed
                      response = requests.get(send_text)
                      print (response.json())		
          else:
              pass
		  
		  
        except:
            continue


def telegram_bot_sendtext(bot_message):
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
   response = requests.get(send_text)
   return response.json()


def Mail(FROM,TO,SUBJECT,TEXT,SERVER):

# Prepare actual message
    message = """\
    From: %s
    To: %s
    Subject: %s
    %s
    """ % (FROM, TO, SUBJECT, TEXT)
# Send the mail
    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, message)
    server.quit()			
			
def parameters():
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7]), (row[8]), (row[9]), (row[10]), (row[11]), (row[12]), (row[13])

    return 0

	
#Check active orders in mysql
def active_orders(marketname):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return int(row[4])

    return 0	



def timestamp_orders(marketname):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return int(row[6])

    return 0



def status_orders(marketname, value):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

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




def percent_serf_max(marketname):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf_max FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0


def percent_serf_min(marketname):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT percent_serf_min FROM orders WHERE active =1 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return float(row[0])
    return 0

	
def buy_time(marketname):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT timestamp FROM orders WHERE active =2 and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0	
	
	
def market_values(marketname, value):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM symbols WHERE symbol = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False	


def format_float(f):
    return "%.4f" % f
	

if __name__ == "__main__":
    main()
