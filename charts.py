import matplotlib as mpl
import matplotlib.pyplot as plt
import io, base64, os, json, re, sys 
import glob
import shutil
import pandas as pd
import numpy as np
import datetime
import warnings
warnings.filterwarnings('ignore')
import yfinance as yf
from yahoo_fin import stock_info as si
from yahoo_fin.stock_info import *
import time
import pymysql
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc




###
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()
days=15

def main():
    print('Starting stock-charts module')

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
          df = df.reset_index(level=['Date'])
#          print (df)
		  
          ohlc_df = df.copy()


          ohlc_df = ohlc_df[['Date', 'Open', 'High', 'Low', 'Close']]
          print (ohlc_df)


         # Converting dates column to float values
          ohlc_df['Date'] = ohlc_df['Date'].map(mdates.date2num)

          fig, ax = plt.subplots(figsize=(8, 4))
          # Converts raw mdate numbers to dates
          ax.xaxis_date()
          plt.xlabel("Date")

          # Making candlestick plot
          candlestick_ohlc(ax, ohlc_df.values, width = 0.8, colorup = 'g', colordown = 'r', alpha = 0.8)
          plt.ylabel("Price")
          plt.title(name)
          plt.grid()
          plt.savefig('/root/PycharmProjects/stock-advisor/images/charts.png')
		  
          newfilename=("{}_chart.png".format(symbol))
          my_path = "/root/PycharmProjects/stock-advisor/images/charts.png"
          new_name = os.path.join(os.path.dirname(my_path), newfilename)
          os.rename(my_path, new_name)

          print (new_name)

          src_dir = "/root/PycharmProjects/stock-advisor/images/"
          dst_dir = "/var/www/html/images/"
          for pngfile in glob.iglob(os.path.join(src_dir, "*.png")):
            shutil.copy(pngfile, dst_dir)



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
