import sys
import os
import re
import pymysql
import pandas as pd
import yfinance as yf
from yahoo_fin import stock_info as si
from yahoo_fin.stock_info import *
from dateutil import parser
import requests
from bs4 import BeautifulSoup
import json
import urllib
from urllib.request import urlopen
import time
import numpy


###
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()
days=3

def main():
    print('Starting stock-prices module')

    prices()




def prices():
    for symbol in symbols: #Loop trough the stock summary
        try:
          symbol=(symbol[0])
#          print (symbol)
          stock = yf.Ticker(symbol)
          hist = stock.history(period="{}d".format(days))
          df = pd.DataFrame(hist)
#          print (df)
          last= (get_live_price(symbol))
          daycurrentopen = (df['Open'][2].tolist())
          daycurrentclose = (df['Close'][2].tolist())
          daycurrentlow = (df['Low'][2].tolist())
          daycurrenthigh = (df['High'][2].tolist())
          dayprevlow = (df['Low'][1].tolist())
          dayprevhigh = (df['High'][1].tolist())
          dayprevopen = (df['Open'][1].tolist())
          dayprevclose = (df['Close'][1].tolist())
          dayprevlow2 = (df['Low'][0].tolist())
          dayprevhigh2 = (df['High'][0].tolist())
          dayprevopen2 = (df['Open'][0].tolist())
          dayprevclose2 = (df['Close'][0].tolist())


          day_candle = 'NONE'
          prevday_candle = 'NONE'
          prevday2_candle = 'NONE'

          if last > daycurrentopen:
              day_candle = 'U'
          else:
              day_candle = 'D'

          if dayprevclose > dayprevopen:
              prevday_candle = 'U'
          else:
              prevday_candle = 'D'

          if dayprevclose2 > dayprevopen2:
              prevday2_candle = 'U'
          else:
              prevday2_candle = 'D'

#          print (symbol, day_candle, prevday_candle, prevday2_candle)     
          

###############
          HAD_PREV_Close2 = (dayprevopen2 + dayprevhigh2 + dayprevlow2 + dayprevclose2) / 4
          HAD_PREV_Open2 = (dayprevopen2 + dayprevclose2) / 2
          HAD_PREV_Low2 = dayprevlow2
          HAD_PREV_High2 = dayprevhigh2


          HAD_PREV_Close = (dayprevopen + dayprevhigh + dayprevlow + dayprevclose) / 4
          HAD_PREV_Open = (HAD_PREV_Open2 + HAD_PREV_Close2) / 2
          elements1 = numpy.array([dayprevhigh, dayprevlow, HAD_PREV_Open, HAD_PREV_Close])
          HAD_PREV_High = elements1.max(0)
          HAD_PREV_Low = elements1.min(0)

          HAD_Close = (daycurrentopen + daycurrenthigh + daycurrentlow + daycurrentclose) / 4
          HAD_Open = (HAD_PREV_Open + HAD_PREV_Close) / 2
          elements0 = numpy.array([daycurrenthigh, daycurrentlow, HAD_Open, HAD_Close])
          HAD_High = elements0.max(0)
          HAD_Low = elements0.min(0)
#############
          HAD_trend = "NONE"
#############
          had_direction_down_short0 =((HAD_High - HAD_Low) / (HAD_Open - HAD_Close) >= 2)  and (HAD_Open - HAD_Close !=0)
          had_direction_down_short1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Open - HAD_PREV_Close) >= 2) and (HAD_PREV_Open - HAD_PREV_Close !=0)
          had_direction_down_short2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Open2 - HAD_PREV_Close2) >= 2) and (HAD_PREV_Open2 - HAD_PREV_Close2 !=0)
          had_direction_down_shorter0 =((HAD_High - HAD_Low) / (HAD_Open - HAD_Close) >= 4)  and (HAD_Open - HAD_Close !=0)
          had_direction_down_shorter1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Open - HAD_PREV_Close) >= 4) and (HAD_PREV_Open - HAD_PREV_Close !=0)
          had_direction_down_shorter2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Open2 - HAD_PREV_Close2) >= 4) and (HAD_PREV_Open2 - HAD_PREV_Close2 !=0)
          had_direction_down0 = (HAD_Close < HAD_Open)
          had_direction_down1 = (HAD_PREV_Close < HAD_PREV_Open)
          had_direction_down2 = (HAD_PREV_Close2 < HAD_PREV_Open2)
          had_direction_down_long_0 = (HAD_Open == HAD_High and HAD_Close < HAD_Open)
          had_direction_down_long_1 = (HAD_PREV_Open == HAD_PREV_High and HAD_PREV_Close < HAD_PREV_Open)
          had_direction_down_long_2 = (HAD_PREV_Open2 == HAD_PREV_High2 and HAD_PREV_Close2 < HAD_PREV_Open2)
          had_direction_down_longer = (numpy.abs(HAD_Open - HAD_Close) > numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and had_direction_down0 and had_direction_down1)
          had_direction_down_longermax = (numpy.abs(HAD_Open - HAD_Close) > numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and numpy.abs(HAD_PREV_Open - HAD_PREV_Close) > numpy.abs(HAD_PREV_Open2 - HAD_PREV_Close2 ) and had_direction_down0 and had_direction_down1 and had_direction_down2)
          had_direction_down_smaller = (numpy.abs(HAD_Open - HAD_Close) < numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and had_direction_down0 and had_direction_down1)
          had_direction_down_smaller1 = (numpy.abs(HAD_PREV_Open - HAD_PREV_Close) < numpy.abs(HAD_PREV_Open2 - HAD_PREV_Close2) and had_direction_down1 and had_direction_down2)
          had_direction_down_smallermax = (numpy.abs(HAD_Open - HAD_Close) < numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and numpy.abs(HAD_PREV_Open - HAD_PREV_Close) < numpy.abs(HAD_PREV_Open2 - HAD_PREV_Close2) and had_direction_down0 and had_direction_down1 and had_direction_down2)

          had_direction_spin0 = (HAD_Open == HAD_Close)
          had_direction_spin1 = (HAD_PREV_Open == HAD_PREV_Close)
          had_direction_spin2 = (HAD_PREV_Open2 == HAD_PREV_Close2)

          had_direction_up_short0 = ((HAD_High - HAD_Low) / (HAD_Close - HAD_Open) >= 2) and (HAD_Close - HAD_Open !=0)
          had_direction_up_short1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Close - HAD_PREV_Open) >= 2) and (HAD_PREV_Close - HAD_PREV_Open !=0)
          had_direction_up_short2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Close2 - HAD_PREV_Open2) >= 2) and (HAD_PREV_Close2 - HAD_PREV_Open2 !=0)
          had_direction_up_shorter0 = ((HAD_High - HAD_Low) / (HAD_Close - HAD_Open) >= 4) and (HAD_Close - HAD_Open !=0)
          had_direction_up_shorter1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Close - HAD_PREV_Open) >= 4) and (HAD_PREV_Close - HAD_PREV_Open !=0)
          had_direction_up_shorter2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Close2 - HAD_PREV_Open2) >= 4) and (HAD_PREV_Close2 - HAD_PREV_Open2 !=0)
          had_direction_up0 = (HAD_Close > HAD_Open)
          had_direction_up1 = (HAD_PREV_Close > HAD_PREV_Open)
          had_direction_up2 = (HAD_PREV_Close2 > HAD_PREV_Open2)
          had_direction_up_long_0 = (HAD_Open == HAD_Low and HAD_Close > HAD_Open)
          had_direction_up_long_1 = (HAD_PREV_Open == HAD_PREV_Low and HAD_PREV_Close > HAD_PREV_Open)
          had_direction_up_long_2 = (HAD_PREV_Open2 == HAD_PREV_Low2 and HAD_PREV_Close2 > HAD_PREV_Open2)
          had_direction_up_longer = (numpy.abs(HAD_Close - HAD_Open) > numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and had_direction_up0 and had_direction_up1)
          had_direction_up_longermax = (numpy.abs(HAD_Close - HAD_Open) > numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and numpy.abs(HAD_PREV_Close - HAD_PREV_Open) > numpy.abs(HAD_PREV_Close2 - HAD_PREV_Open2) and had_direction_up0 and had_direction_up1 and had_direction_up2)
          had_direction_up_smaller = (numpy.abs(HAD_Close - HAD_Open) < numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and had_direction_up0 and had_direction_up1)
          had_direction_up_smaller1 = (numpy.abs(HAD_PREV_Close - HAD_PREV_Open) < numpy.abs(HAD_PREV_Close2 - HAD_PREV_Open2) and had_direction_up1 and had_direction_up2)
          had_direction_up_smallermax = (numpy.abs(HAD_Close - HAD_Open) < numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and numpy.abs(HAD_PREV_Close - HAD_PREV_Open) < numpy.abs(HAD_PREV_Close2 - HAD_PREV_Open2) and had_direction_up0 and had_direction_up1 and had_direction_up2)



#####

          if (((had_direction_down_long_0 and had_direction_down0) or (had_direction_down_long_0 and had_direction_down_long_1 and had_direction_down0) or (had_direction_down_long_0 or had_direction_down_long_1 and had_direction_down_longer) or (had_direction_down_long_0 or had_direction_down_long_1 and had_direction_down_longermax and had_direction_down_longer) and had_direction_down0) or (had_direction_down0 and had_direction_down1 and had_direction_down2)):
               had_trend = "DOWN"
          if (((had_direction_up_long_0 and had_direction_up0) or (had_direction_up_long_0 and had_direction_up_long_1 and had_direction_up0) or (had_direction_up_long_0 or had_direction_up_long_1 and had_direction_up_longer) or (had_direction_up_long_0 or had_direction_up_long_1 and had_direction_up_longer and had_direction_up_longermax) and had_direction_up0) or (had_direction_up0 and had_direction_up1 and had_direction_up2)):
               had_trend = "UP"
          if ((had_direction_up_short2 and had_direction_spin1 and had_direction_up0) or (had_direction_down_short2 and had_direction_up_short1 and had_direction_up_long_0) or (had_direction_down2 and had_direction_down_short1 and had_direction_spin0) or (had_direction_down_long_2 and had_direction_down_short1 and had_direction_up_long_0) or (had_direction_down_long_2 and had_direction_up_short1 and had_direction_up_long_0) or (had_direction_down2 and had_direction_up_long_0 and had_direction_up1 and had_direction_up_longer) or (had_direction_down_long_2 and had_direction_down_smaller1 and had_direction_up0) or (had_direction_down_long_2 and had_direction_down_short1 and  had_direction_up_long_0) or (had_direction_down_longermax and had_direction_up_short0) and had_direction_down1 and had_direction_down2):
               had_trend = "Revers-UP"
          if ((had_direction_down_short2 and had_direction_spin1 and had_direction_down0) or (had_direction_up_short2 and had_direction_down_short1 and had_direction_down_long_0) or (had_direction_up2 and had_direction_up_short1 and had_direction_spin0) or (had_direction_up_long_2 and had_direction_up_short1 and had_direction_down_long_0) or (had_direction_up_long_2 and had_direction_down_short1 and had_direction_down_long_0) or (had_direction_up2 and had_direction_down_long_0 and had_direction_down1 and had_direction_down_longer) or (had_direction_up_long_2 and had_direction_up_smaller1 and had_direction_down0) or (had_direction_up_long_2 and had_direction_up_short1 and  had_direction_down_long_0) or (had_direction_up_longermax and had_direction_down_short0) and had_direction_up1 and had_direction_up2):
               had_trend = "Revers-DOWN"
          if  had_trend != "Revers-DOWN" and   had_trend != "Revers-UP" and  had_trend != "DOWN" and had_trend != "UP":
               had_trend = "STABLE"  




          print (symbol, had_trend, day_candle, last)


          try:
              db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
              cursor = db.cursor()
              cursor.execute('update symbols set current_price=%s, heikin_ashi=%s, candle_direction=%s where symbol=%s',(last, had_trend, day_candle, symbol))
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



