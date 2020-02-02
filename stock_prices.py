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
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
import matplotlib as mpl
import matplotlib.pyplot as plt
import glob
import shutil
import warnings
warnings.filterwarnings('ignore')
import time
import datetime
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")
currentdate = now.strftime("%Y-%m-%d")

###
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()
days=15

def main():
    print('Starting stock-prices module')

    prices()




def prices():
    for symbol in symbols: #Loop trough the stock summary
        try:
          symbol=(symbol[0])
          name=symbol_full_name(symbol, 3)
#          print (symbol)
          stock = yf.Ticker(symbol)
          hist = stock.history(period="{}d".format(days))
          df = pd.DataFrame(hist)
          print (df)
          last= (get_live_price(symbol))
          daycurrentopen = (df['Open'][4].tolist())
          daycurrentclose = (df['Close'][4].tolist())
          daycurrentlow = (df['Low'][4].tolist())
          daycurrenthigh = (df['High'][4].tolist())
          dayprevlow = (df['Low'][3].tolist())
          dayprevhigh = (df['High'][3].tolist())
          dayprevopen = (df['Open'][3].tolist())
          dayprevclose = (df['Close'][3].tolist())
          dayprevlow2 = (df['Low'][2].tolist())
          dayprevhigh2 = (df['High'][2].tolist())
          dayprevopen2 = (df['Open'][2].tolist())
          dayprevclose2 = (df['Close'][2].tolist())
          dayprevlow3 = (df['Low'][1].tolist())
          dayprevhigh3 = (df['High'][1].tolist())
          dayprevopen3 = (df['Open'][1].tolist())
          dayprevclose3 = (df['Close'][1].tolist())
          dayprevlow4 = (df['Low'][0].tolist())
          dayprevhigh4 = (df['High'][0].tolist())
          dayprevopen4 = (df['Open'][0].tolist())
          dayprevclose4 = (df['Close'][0].tolist())
		  
		  
          df = df.reset_index(level=['Date'])

          
          daycurrentdate = (df['Date'][14]).date()
          dayprevdate = (df['Date'][13]).date()
          dayprevdate2 = (df['Date'][12]).date()
          dayprevdate3 = (df['Date'][11]).date()
          dayprevdate4 = (df['Date'][10]).date()
          dayprevdate5 = (df['Date'][9]).date()
          dayprevdate6 = (df['Date'][8]).date()
          dayprevdate7 = (df['Date'][7]).date()          
          dayprevdate8 = (df['Date'][6]).date()
          dayprevdate9 = (df['Date'][5]).date()
          dayprevdate10 = (df['Date'][4]).date()
          dayprevdate11 = (df['Date'][3]).date()
          dayprevdate12 = (df['Date'][2]).date()          
          dayprevdate13 = (df['Date'][1]).date()
          dayprevdate14 = (df['Date'][0]).date()		  
		  
		  
		  
		  
#          print (df)
          heikin_ashi_df = heikin_ashi(df)
	  
          
		  
	  
		  
		  
		  
          

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




          HAD_PREV_Close4 = (dayprevopen4 + dayprevhigh4 + dayprevlow4 + dayprevclose4) / 4
          HAD_PREV_Open4 = (dayprevopen4 + dayprevclose4) / 2
          HAD_PREV_Low4 = dayprevlow4
          HAD_PREV_High4 = dayprevhigh4
		  
          HAD_PREV_Close3 = (dayprevopen3 + dayprevhigh3 + dayprevlow3 + dayprevclose3) / 4
          HAD_PREV_Open3 = (HAD_PREV_Open4 + HAD_PREV_Close4) / 2
          elements3 = numpy.array([dayprevhigh3, dayprevlow3, HAD_PREV_Open4, HAD_PREV_Close4])
          HAD_PREV_High3 = elements3.max(0)
          HAD_PREV_Low3 = elements3.min(0)

          HAD_PREV_Close2 = (dayprevopen2 + dayprevhigh2 + dayprevlow2 + dayprevclose2) / 4
          HAD_PREV_Open2 = (HAD_PREV_Open3 + HAD_PREV_Close3) / 2
          elements2 = numpy.array([dayprevhigh2, dayprevlow2, HAD_PREV_Open3, HAD_PREV_Close3])
          HAD_PREV_High2 = elements2.max(0)
          HAD_PREV_Low2 = elements2.min(0)

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
		  
		  
		  
		  
		  
          d = {'Date': [dayprevdate4, dayprevdate3, dayprevdate2, dayprevdate, daycurrentdate], 'Open': [HAD_PREV_Open4, HAD_PREV_Open3, HAD_PREV_Open2, HAD_PREV_Open, HAD_Open], 'High': [HAD_PREV_High4, HAD_PREV_High3, HAD_PREV_High2, HAD_PREV_High, HAD_High], 'Low': [HAD_PREV_Low4, HAD_PREV_Low3, HAD_PREV_Low2, HAD_PREV_Low, HAD_Low], 'Close': [HAD_PREV_Close4, HAD_PREV_Close3, HAD_PREV_Close2, HAD_PREV_Close, HAD_Close]}
          dfha = pd.DataFrame(data=d)
		  
#          ohlc_df = dfha.copy()
          ohlc_df = heikin_ashi_df.copy()
          date=[dayprevdate14, dayprevdate13, dayprevdate12, dayprevdate11, dayprevdate10, dayprevdate9, dayprevdate8, dayprevdate7, dayprevdate6, dayprevdate5, dayprevdate4, dayprevdate3, dayprevdate2, dayprevdate, daycurrentdate]	
          ohlc_df['Date']=date
          		  

          ohlc_df = ohlc_df[['Date', 'Open', 'High', 'Low', 'Close']]
          print (ohlc_df)


         # Converting dates column to float values
          ohlc_df['Date'] = ohlc_df['Date'].map(mdates.date2num)

          fig, ax = plt.subplots(figsize=(8, 4))


		 
          # Making candlestick plot
          candlestick_ohlc(ax, ohlc_df.values, width = 0.8, colorup = 'g', colordown = 'r', alpha = 0.8)
          plt.title(name)
          plt.grid()
          plt.savefig('/root/PycharmProjects/stock-advisor/images/hacharts.png')
		  
          newfilename=("{}_hachart.png".format(symbol))
          my_path = "/root/PycharmProjects/stock-advisor/images/hacharts.png"
          new_name = os.path.join(os.path.dirname(my_path), newfilename)
          os.rename(my_path, new_name)

          print (new_name)

          src_dir = "/root/PycharmProjects/stock-advisor/images/"
          dst_dir = "/var/www/html/images/"
          for pngfile in glob.iglob(os.path.join(src_dir, "*.png")):
            shutil.copy(pngfile, dst_dir)	   
		  
		  
		  
		  
		  
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
              cursor.execute("update symbols set current_price='%s', heikin_ashi='%s', candle_direction='%s'  where symbol='%s'" % (last, had_trend, day_candle, symbol))
              cursor.execute("update history set price='%s' where symbol='%s' and date='%s'" % (daycurrentclose, symbol, currentdate))			  
              db.commit()
          except pymysql.Error as e:
              print ("Error %d: %s" % (e.args[0], e.args[1]))
              sys.exit(1)
          finally:
              db.close()


        except:
            continue


def heikin_ashi(df):
    heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['Open', 'High', 'Low', 'Close'])
    
    heikin_ashi_df['Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    
    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 0] = df['Open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i-1, 0] + heikin_ashi_df.iat[i-1, 3]) / 2
        
    heikin_ashi_df['High'] = heikin_ashi_df.loc[:, ['Open', 'Close']].join(df['High']).max(axis=1)
    
    heikin_ashi_df['Low'] = heikin_ashi_df.loc[:, ['Open', 'Close']].join(df['Low']).min(axis=1)
    
    return heikin_ashi_df


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



