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
dayid=days-1

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
          daycurrentopen = (df['Open'][14].tolist())
          daycurrentclose = (df['Close'][14].tolist())
          daycurrentlow = (df['Low'][14].tolist())
          daycurrenthigh = (df['High'][14].tolist())
          dayprevlow = (df['Low'][13].tolist())
          dayprevhigh = (df['High'][13].tolist())
          dayprevopen = (df['Open'][13].tolist())
          dayprevclose = (df['Close'][13].tolist())
          dayprevlow2 = (df['Low'][12].tolist())
          dayprevhigh2 = (df['High'][12].tolist())
          dayprevopen2 = (df['Open'][12].tolist())
          dayprevclose2 = (df['Close'][12].tolist())
          dayprevlow3 = (df['Low'][11].tolist())
          dayprevhigh3 = (df['High'][11].tolist())
          dayprevopen3 = (df['Open'][11].tolist())
          dayprevclose3 = (df['Close'][11].tolist())
          dayprevlow4 = (df['Low'][10].tolist())
          dayprevhigh4 = (df['High'][10].tolist())
          dayprevopen4 = (df['Open'][10].tolist())
          dayprevclose4 = (df['Close'][10].tolist())
          #print (df['Open'][14].tolist())		  
		  
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
          candle_dir='NONE'
		  


   		  
          if last > daycurrentopen and last > dayprevclose:
              candle_dir = 'U'
          else:
              candle_dir = 'D'

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


  
          


		  
		  
		  
		  
		  
#          d = {'Date': [dayprevdate4, dayprevdate3, dayprevdate2, dayprevdate, daycurrentdate], 'Open': [HAD_PREV_Open4, HAD_PREV_Open3, HAD_PREV_Open2, HAD_PREV_Open, HAD_Open], 'High': [HAD_PREV_High4, HAD_PREV_High3, HAD_PREV_High2, HAD_PREV_High, HAD_High], 'Low': [HAD_PREV_Low4, HAD_PREV_Low3, HAD_PREV_Low2, HAD_PREV_Low, HAD_Low], 'Close': [HAD_PREV_Close4, HAD_PREV_Close3, HAD_PREV_Close2, HAD_PREV_Close, HAD_Close]}
#          dfha = pd.DataFrame(data=d)
		  
#          ohlc_df = dfha.copy()
          ohlc_df = heikin_ashi_df.copy()
          date=[dayprevdate14, dayprevdate13, dayprevdate12, dayprevdate11, dayprevdate10, dayprevdate9, dayprevdate8, dayprevdate7, dayprevdate6, dayprevdate5, dayprevdate4, dayprevdate3, dayprevdate2, dayprevdate, daycurrentdate]	
          ohlc_df['Date']=date
          		  

          ohlc_df = ohlc_df[['Date', 'Open', 'High', 'Low', 'Close']]
          #print (ohlc_df)



         # Converting dates column to float values
          ohlc_df['Date'] = ohlc_df['Date'].map(mdates.date2num)

          fig, ax = plt.subplots(figsize=(8, 4))
          ax.xaxis_date()

		 
          # Making candlestick plot
          candlestick_ohlc(ax, ohlc_df.values, width = 0.8, colorup = 'g', colordown = 'r', alpha = 0.8)
          plt.title(name)
          plt.gcf().autofmt_xdate()   # Beautify the x-labels
          plt.autoscale(tight=True)
          plt.grid()
          ax.grid(True)
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
		  
		  
		  
###############




          HAD_PREV_Close4 = ohlc_df['Close'][dayid-4]
          HAD_PREV_Open4 = ohlc_df['Open'][dayid-4]
          HAD_PREV_Low4 = ohlc_df['High'][dayid-4]
          HAD_PREV_High4 = ohlc_df['Low'][dayid-4]
		  
          HAD_PREV_Close3 = ohlc_df['Close'][dayid-3]
          HAD_PREV_Open3 = ohlc_df['Open'][dayid-3]
          HAD_PREV_High3 = ohlc_df['High'][dayid-3]
          HAD_PREV_Low3 = ohlc_df['Low'][dayid-3]

          HAD_PREV_Close2 = ohlc_df['Close'][dayid-2]
          HAD_PREV_Open2 = ohlc_df['Open'][dayid-2]
          HAD_PREV_High2 = ohlc_df['High'][dayid-2]
          HAD_PREV_Low2 = ohlc_df['Low'][dayid-2]

          HAD_PREV_Close = ohlc_df['Close'][dayid-1]
          HAD_PREV_Open = ohlc_df['Open'][dayid-1]
          HAD_PREV_High = ohlc_df['High'][dayid-1]
          HAD_PREV_Low = ohlc_df['Low'][dayid-1]

          HAD_Close = ohlc_df['Close'][dayid]
          HAD_Open = ohlc_df['Open'][dayid]
          HAD_High = ohlc_df['High'][dayid]
          HAD_Low = ohlc_df['Low'][dayid]
		  
		  
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



          try:
              db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
              cursor = db.cursor()
              cursor.execute("update symbols set current_price='%s', candle_direction='%s'  where symbol='%s'" % (last, candle_dir, symbol))
              cursor.execute("update history set price='%s' where symbol='%s' and date='%s'" % (last, symbol, currentdate))
              db.commit()
          except pymysql.Error as e:
              print ("Error %d: %s" % (e.args[0], e.args[1]))
              sys.exit(1)
          finally:
              db.close()
#####

          if (((had_direction_down_long_0 and had_direction_down0) or (had_direction_down_long_0 and had_direction_down_long_1 and had_direction_down0) or (had_direction_down_long_0 or had_direction_down_long_1 and had_direction_down_longer) or (had_direction_down_long_0 or had_direction_down_long_1 and had_direction_down_longermax and had_direction_down_longer) and had_direction_down0) or (had_direction_down0 and had_direction_down1 and had_direction_down2)):
               had_trend = "DOWN"
          elif (((had_direction_up_long_0 and had_direction_up0) or (had_direction_up_long_0 and had_direction_up_long_1 and had_direction_up0) or (had_direction_up_long_0 or had_direction_up_long_1 and had_direction_up_longer) or (had_direction_up_long_0 or had_direction_up_long_1 and had_direction_up_longer and had_direction_up_longermax) and had_direction_up0) or (had_direction_up0 and had_direction_up1 and had_direction_up2)):
               had_trend = "UP"
          elif ((had_direction_up_short2 and had_direction_spin1 and had_direction_up0) or (had_direction_down_short2 and had_direction_up_short1 and had_direction_up_long_0) or (had_direction_down2 and had_direction_down_short1 and had_direction_spin0) or (had_direction_down_long_2 and had_direction_down_short1 and had_direction_up_long_0) or (had_direction_down_long_2 and had_direction_up_short1 and had_direction_up_long_0) or (had_direction_down2 and had_direction_up_long_0 and had_direction_up1 and had_direction_up_longer) or (had_direction_down_long_2 and had_direction_down_smaller1 and had_direction_up0) or (had_direction_down_long_2 and had_direction_down_short1 and  had_direction_up_long_0) or (had_direction_down_longermax and had_direction_up_short0) and had_direction_down1 and had_direction_down2):
               had_trend = "Revers-UP"
          elif ((had_direction_down_short2 and had_direction_spin1 and had_direction_down0) or (had_direction_up_short2 and had_direction_down_short1 and had_direction_down_long_0) or (had_direction_up2 and had_direction_up_short1 and had_direction_spin0) or (had_direction_up_long_2 and had_direction_up_short1 and had_direction_down_long_0) or (had_direction_up_long_2 and had_direction_down_short1 and had_direction_down_long_0) or (had_direction_up2 and had_direction_down_long_0 and had_direction_down1 and had_direction_down_longer) or (had_direction_up_long_2 and had_direction_up_smaller1 and had_direction_down0) or (had_direction_up_long_2 and had_direction_up_short1 and  had_direction_down_long_0) or (had_direction_up_longermax and had_direction_down_short0) and had_direction_up1 and had_direction_up2):
               had_trend = "Revers-DOWN"
          else:
               had_trend = "STABLE"  




          print (symbol, had_trend, candle_dir)


          try:
              db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
              cursor = db.cursor()
              cursor.execute("update symbols set heikin_ashi='%s'  where symbol='%s'" % (had_trend, symbol))		  
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



