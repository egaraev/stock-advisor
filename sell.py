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
    print('Starting stock sell  module')


    Sell()


def Sell():
    for symbol in symbols: #Loop trough the stock summary
        try:
          market=(symbol[0])
          print (market)
          stock = yf.Ticker(market)
          last= float("{0:.4f}".format(si.get_live_price(market)))
          hist = stock.history(period="1d")
          df = pd.DataFrame(hist)
          #print (last)
          day_close = (df['Close'][0].tolist())
          buy_size = parameters()[0] #The size for opening orders for STOP_LOSS mode
          stop_bot_force = parameters()[4]  #If stop_bot_force==1 we  stop bot and close all orders
          stop_bot = parameters()[10]
          #print (stop_bot_force)
          currtime = int(time.time())
          debug_mode=parameters()[9]
          max_orders = parameters()[5]
          bot_token= parameters()[11]
          bot_chatID= parameters()[12]
          #print (bot_token, bot_chatID)
          print ("Global sell parameters configured, moving to market loop")
          #dayofweek=weekday()		  
          timestamp = int(time.time())
          #How much market has been changed
          percent_chg = float("{0:.4f}".format(((last / day_close) - 1) * 100))
          #HOW MUCH TO BUY
          buy_quantity = float("{0:.4f}".format(buy_size / last))
          bought_price_sql = float(status_orders(market, 3))
          bought_quantity_sql = float(status_orders(market, 2))
          sell_quantity_sql = bought_quantity_sql
          active = active_orders(market)
          timestamp_old = int(timestamp_orders(market))
          now = datetime.datetime.now()
          today = datetime.datetime.now().date()
#          print (today)
          currenttime = now.strftime("%Y-%m-%d %H:%M")
          heikin_ashi=market_values(market,5)
          candle_direction=market_values(market,7)
          hour_candle_direction=market_values(market,21)
          tweet_positive=market_values(market,8)
          tweet_negative=market_values(market,9)
          tweet_ratio = float("{0:.2f}".format(tweet_positive/tweet_negative))
          #print (tweet_ratio)
          danger_order=status_orders(market, 29)
          
          ai_price=market_values(market,11)
          ai_direction=market_values(market,24)
             
          tweet_polarity=market_values(market,13)
          tweet_score=market_values(market,15)
          candle_score=market_values(market,17)
          news_score=market_values(market,20)
          candle_pattern=market_values(market,18)
          trend = str(market_values(market,23))
          #print (heikin_ashi, candle_direction,tweet_positive,tweet_negative,tweet_polarity,tweet_score,candle_score )
          macd = str(market_values(market,26))				
          obv = str(market_values(market,25))

		  
          print ("Market parameters configured, moving to sell for ", market)		  

          try:
               db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
               cursor = db.cursor()
               serf = float("{0:.4f}".format(last * bought_quantity_sql - bought_price_sql * bought_quantity_sql))
               #print (last,bought_price_sql,bought_quantity_sql )

               if bought_price_sql!=0:
                   procent_serf = float("{0:.4f}".format(((last / bought_price_sql) - 1) * 100))
                   #print (market, procent_serf)

                   if procent_serf>=percent_serf_max(market):
                       cursor.execute("update orders set percent_serf_max=%s where market = %s and active =1 and open_sell=0 ",(procent_serf, market))
                   elif procent_serf<percent_serf_min(market):
                       cursor.execute("update orders set percent_serf_min=%s where market = %s and active =1 and open_sell=0 ",(procent_serf, market))
                   else:
                       cursor.execute("update orders set percent_serf=%s where market = %s and active =1 and open_sell=0 ",(procent_serf, market))
               
               if percent_serf_min(market)<(-5):
                    cursor.execute("update orders set danger_order = %s where market = %s and active =1" , (1, market))
               if percent_serf_max(market)>2.5:
                    cursor.execute("update orders set danger_order = %s where market = %s and active =1" , (0, market))
               cursor.execute("update orders set serf_usd = %s where market = %s and active =1", (serf, market))	   
               cursor.execute('update symbols set current_price = %s  where symbol = %s and active =1', (last, market))
               db.commit()
               
          except pymysql.Error as e:
               print ("Error %d: %s" % (e.args[0], e.args[1]))
               sys.exit(1)
          finally:
               db.close()


          max_percent_sql = float("{0:.2f}".format(status_orders(market, 15)))
          min_percent_sql = float("{0:.2f}".format(status_orders(market, 24)))
          print ("Updated serf and procent serf stuff for", market)


		  
          print ("Starting selling mechanizm for " , market)

		  
          if stop_bot_force==1 and (bought_quantity_sql is not None and bought_quantity_sql != 0.0):
                  print ('    1 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting or loosing  ' + str(format_float(serf)) + ' USD')
                  printed=('    1 Force_stop_bot - Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting or loosing  ' + str(format_float(procent_serf)) + ' %')
                  try:
                      db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                      cursor = db.cursor()
                      cursor.execute('insert into logs(date, entry) values("%s", "%s")' % (currenttime, printed))
                      cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("1 , Force_stop_bot p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(heikin_ashi) + '  Candle_direction: ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score) + ' Candle_pattern: ' + str(candle_pattern) + ' News_score: ' + str(news_score)+ ' H_candle_dir: ' + str(hour_candle_direction) + ' Trend: ' + str(trend) +' MACD: ' +str(macd)  +' OBV: ' +str(obv) +' MACD: ' +str(macd)  +' OBV: ' +str(obv),currtime, market))
                      cursor.execute('update orders set active = 0 where market =("%s")' % market)
                      netto_value=format_float(procent_serf-0)
                      cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                      newvalue = format_float(summ_serf() + (procent_serf-0))					  
                      cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                      cursor.execute('update symbols set date = %s  where symbol = %s and active =1', (today, market))					  
                      db.commit()
                  except pymysql.Error as e:
                      print ("Error %d: %s" % (e.args[0], e.args[1]))
                      sys.exit(1)
                  finally:
                      db.close()
                  #Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")					  
                  send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + printed
                  response = requests.get(send_text)
                  print (response.json())				  

          #print ("Starting selling mechanizm for ", market)
          
          if bought_price_sql != None:
               if bought_quantity_sql is None or bought_quantity_sql == 0.0:
                     # print market, bought_quantity_sql, current_balance
                    pass
                            # If curent balance of this currency more then zero
               elif bought_quantity_sql > 0:				  
               	  		
			
                 if ((2.0>procent_serf>=0.7 and danger_order==1 and max_percent_sql - procent_serf >= 0.3) or  (max_percent_sql - procent_serf >= 0.8 and 5>=procent_serf >= 2 and candle_direction=='D' )   or (max_percent_sql - procent_serf >= 1.5 and 9>=procent_serf >= 5 and candle_direction=='D' and hour_candle_direction=='D')):
                      print ('    5  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting  ' + str(format_float(serf)) + ' USD')
                      printed = ('  Taking into account current situation on the market, I would advise to sell all our stocks of ' + market + ' for this current price ' + str(format_float(last)) + '  and get   ' + str(format_float(procent_serf)) + ' %' +' For more details go here: http://139.162.132.189')
                      try:

                          db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                          cursor = db.cursor()
                          cursor.execute('insert into logs(date, entry) values("%s", "%s")' % (currenttime, printed))
                          cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("5 , Floating_TP   p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(heikin_ashi) + '  Candle_direction: ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) +' Tweet_ratio: ' +str(tweet_ratio) + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score)+ ' Candle_pattern: ' + str(candle_pattern)+ ' News_score: ' + str(news_score)+  ' H_candle_dir: ' + str(hour_candle_direction)  + ' Trend: ' + str(trend) +' MACD: ' +str(macd)  +' OBV: ' +str(obv),currtime, market))
                          cursor.execute('update orders set active = 0 where market =("%s")' % market)
                          netto_value=format_float(procent_serf-0)
                          cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                          newvalue = format_float(summ_serf() + (procent_serf-0))					  
                          cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                          cursor.execute('update symbols set date = %s  where symbol = %s and active =1', (today, market))		  
                          db.commit()
                      except pymysql.Error as e:
                          print ("Error %d: %s" % (e.args[0], e.args[1]))
                          sys.exit(1)
                      finally:
                          db.close()
                      #Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                      send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + printed
                      response = requests.get(send_text)
                      print (response.json())
				  


                 if  procent_serf>=10:
                      print ('    3 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting  ' + str(format_float(serf)) + ' USD')
                      printed = ('    Wow wow, holy shit, we just reached our take profit. Lets sell all our units of ' + market + ' for this great price ' + str(format_float(last)) + '  and get   ' + str(format_float(procent_serf)) + ' % ' +' For more details go here: http://139.162.132.189')
                      try:

                          db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                          cursor = db.cursor()
                          cursor.execute('insert into logs(date, entry) values("%s", "%s")' % (currenttime, printed))
                          cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("3 , Fixed_TP p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(heikin_ashi) + '  Candle_direction: ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) +' Tweet_ratio: ' +str(tweet_ratio) + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score)+ ' Candle_pattern: ' + str(candle_pattern)+ ' News_score: ' + str(news_score)+  ' H_candle_dir: ' + str(hour_candle_direction)  + ' Trend: ' + str(trend) +' MACD: ' +str(macd)  +' OBV: ' +str(obv) +' MACD: ' +str(macd)  +' OBV: ' +str(obv),currtime, market))
                          cursor.execute('update orders set active = 0 where market =("%s")' % market)
                          netto_value=format_float(procent_serf-0)
                          cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                          newvalue = format_float(summ_serf() + (procent_serf-0))					  
                          cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                          cursor.execute('update symbols set date = %s  where symbol = %s and active =1', (today, market))					  
                          db.commit()
                      except pymysql.Error as e:
                          print ("Error %d: %s" % (e.args[0], e.args[1]))
                          sys.exit(1)
                      finally:
                          db.close()
                      #Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell, TP", printed, "localhost")
                      send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + printed
                      response = requests.get(send_text)
                      print (response.json())

                 if  procent_serf <= -7.5  and  percent_serf_max(market) < 0.1  and candle_direction=='D' and heikin_ashi!="UP" and heikin_ashi!="Revers-UP" and candle_score<=0:
                      print ('    2  -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting  ' + str(format_float(serf)) + ' USD')
                      printed = ('  Lets sell all this shitty ' + market + ' for this current price ' + str(format_float(last)) + '  and we will lose only  ' + str(format_float(procent_serf)) + ' %, otherwise we can lose much more ' +' For more details go here: http://139.162.132.189')
                      try:

                          db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                          cursor = db.cursor()
                          cursor.execute('insert into logs(date, entry) values("%s", "%s")' % (currenttime, printed))
                          cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("2 , Floating_SL  p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(heikin_ashi) + '  Candle_direction: ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) +' Tweet_ratio: ' +str(tweet_ratio) + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score)+ ' Candle_pattern: ' + str(candle_pattern)+ ' News_score: ' + str(news_score)+  ' H_candle_dir: ' + str(hour_candle_direction) + ' Trend: ' + str(trend) +' MACD: ' +str(macd)  +' OBV: ' +str(obv),currtime, market))
                          cursor.execute('update orders set active = 0 where market =("%s")' % market)
                          netto_value=format_float(procent_serf-0)
                          cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                          newvalue = format_float(summ_serf() + (procent_serf-0))					  
                          cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                          cursor.execute('update symbols set date = %s  where symbol = %s and active =1', (today, market))					  
                          db.commit()
                      except pymysql.Error as e:
                          print ("Error %d: %s" % (e.args[0], e.args[1]))
                          sys.exit(1)
                      finally:
                          db.close()
                      #Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell", printed, "localhost")
                      send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + printed
                      response = requests.get(send_text)
                      print (response.json())
		
                 if  procent_serf <= -15:
                      print ('    4 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting  ' + str(format_float(serf)) + ' USD')
                      printed = ('    Fuck, we fucked up, we reached our Stop Loss, so to avoid complete disaster lets sell all this shit  ' + market + ' for this crappy price ' + str(format_float(last)) + '  and lose  ' + str(format_float(procent_serf)) + ' % . Fuck fuck!! ' +' For more details go here: http://139.162.132.189')
                      try:

                          db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                          cursor = db.cursor()
                          cursor.execute('insert into logs(date, entry) values("%s", "%s")' % (currenttime, printed))
                          cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("4 , Fixed_SL p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(heikin_ashi) + '  Candle_direction: ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) +' Tweet_ratio: ' +str(tweet_ratio) + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score)+ ' Candle_pattern: ' + str(candle_pattern)+ ' News_score: ' + str(news_score)+  ' H_candle_dir: ' + str(hour_candle_direction) + ' Trend: ' + str(trend) +' MACD: ' +str(macd)  +' OBV: ' +str(obv),currtime, market))
                          cursor.execute('update orders set active = 0 where market =("%s")' % market)
                          netto_value=format_float(procent_serf-0)
                          cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                          newvalue = format_float(summ_serf() + (procent_serf-0))					  
                          cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                          cursor.execute('update symbols set date = %s  where symbol = %s and active =1', (today, market))					  
                          db.commit()
                      except pymysql.Error as e:
                          print ("Error %d: %s" % (e.args[0], e.args[1]))
                          sys.exit(1)
                      finally:
                          db.close()
                      #Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell, SL", printed, "localhost")
                      send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + printed
                      response = requests.get(send_text)
                      print (response.json())
			
			
                 if  (1.0>procent_serf>=-5 and danger_order==1 and candle_direction=='D' and percent_serf_min(market) <= -10 and timestamp-timestamp_old >=2500000) or (1.0>procent_serf>=-7.5 and danger_order==1 and candle_direction=='D' and hour_candle_direction=='D' and percent_serf_min(market) <= -12 and timestamp-timestamp_old >=3500000 and (candle_score<0 or news_score<0)):
                      print ('    6 -Selling ' + str(format_float(sell_quantity_sql)) + ' units of ' + market + ' for ' + str(format_float(last)) + '  and getting  ' + str(format_float(serf)) + ' USD')
                      printed = ('    We have this negative order for more then 1 month, so to avoid  disaster lets sell all this shit with small loses  ' + market + ' for this crappy price ' + str(format_float(last)) + '  and lose  ' + str(format_float(procent_serf)) + ' % . Buying this shit was a mistake ' +' For more details go here: http://139.162.132.189')
                      try:

                          db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                          cursor = db.cursor()
                          cursor.execute('insert into logs(date, entry) values("%s", "%s")' % (currenttime, printed))
                          cursor.execute('update orders set reason_close =%s, sell_time=%s where active=1 and market =%s', ("6 , Long_lasting_SL p:    " + str(format_float(last)) + "    t:   " + str(currenttime)  +'  HA: ' + str(heikin_ashi) + '  Candle_direction: ' + str(candle_direction) + ' Candle_score: ' + str(candle_score) + ' AI_direction: ' + str(ai_direction) + ' Tweet_positive: ' + str(tweet_positive) + ' Tweet_negative: ' + str(tweet_negative) +' Tweet_ratio: ' +str(tweet_ratio) + ' Tweet_polarity: ' + str(tweet_polarity) + ' Tweet_score: ' + str(tweet_score)+ ' Candle_pattern: ' + str(candle_pattern)+ ' News_score: ' + str(news_score)+  ' H_candle_dir: ' + str(hour_candle_direction) + ' Trend: ' + str(trend) +' MACD: ' +str(macd)  +' OBV: ' +str(obv),currtime, market))
                          cursor.execute('update orders set active = 0 where market =("%s")' % market)
                          netto_value=format_float(procent_serf-0)
                          cursor.execute('UPDATE orders SET percent_serf = %s WHERE active = 0 AND market =%s ORDER BY order_id DESC LIMIT 1', (netto_value,market))
                          newvalue = format_float(summ_serf() + (procent_serf-0))					  
                          cursor.execute('insert into statistics(date, serf, market) values("%s", "%s", "%s")' % (currenttime, newvalue, market))
                          cursor.execute('update symbols set date = %s  where symbol = %s and active =1', (today, market))					  
                          db.commit()
                      except pymysql.Error as e:
                          print ("Error %d: %s" % (e.args[0], e.args[1]))
                          sys.exit(1)
                      finally:
                          db.close()
                      #Mail("egaraev@gmail.com", "egaraev@gmail.com", "New sell, SL", printed, "localhost")
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

	
	
def summ_serf():
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    # market=marketname
    cursor.execute("SELECT SUM(percent_serf) FROM orders where active=0")
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return float("{0:.2f}".format(row[0]))
            # return 0
        else:
            return 0	
	

def format_float(f):
    return "%.4f" % f
	

if __name__ == "__main__":
    main()
