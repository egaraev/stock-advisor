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
          ohlc_df = df.copy()
          ohlc_df = ohlc_df[['Date', 'Open', 'High', 'Low', 'Close']]
		  
          df=candle_df(df)
          print (df)
        
          buy_df = df.copy() 
          candle_scored_buy= buy_df[(buy_df['candle_score'] > 0)]
          #print (symbol, candle_scored_buy)
          candle_scored_sell= df[(df['candle_score'] < 0)]		  
          labels_buy=(buy_df['candle_pattern'])
		  			 
		     
		  
		  
          #print (ohlc_df)
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
		  
		  
          ax2 = ax.twinx()
          #plt.plot(ohlc_df['Date'], ohlc_df['Close'], linestyle = '--', linewidth = 1, c='black')
          ax2.plot(candle_scored_buy['Date'], candle_scored_buy['candle_score'],  '^', markersize=15)
          ax2.plot(candle_scored_sell['Date'], candle_scored_sell['candle_score'], 'v', markersize=15)

#          ax2 = df.plot(kind='scatter',x=candle_scored_buy['Date'],y=candle_scored_buy['candle_score'])
#          buy_df[['Date','candle_score','candle_pattern']].apply(lambda row: ax2.text(*row),axis=1);
          #ax2.set_ylim(-4, 4)
		  
          plt.gcf().autofmt_xdate()   # Beautify the x-labels
          plt.autoscale(tight=True)
          plt.grid()
          plt.savefig('/root/PycharmProjects/stock-advisor/images/candlesticks.png')
		  
          newfilename=("{}_candlesticks.png".format(symbol))
          my_path = "/root/PycharmProjects/stock-advisor/images/candlesticks.png"
          new_name = os.path.join(os.path.dirname(my_path), newfilename)
          os.rename(my_path, new_name)

          print (new_name)

          src_dir = "/root/PycharmProjects/stock-advisor/images/"
          dst_dir = "/var/www/html/images/"
          for pngfile in glob.iglob(os.path.join(src_dir, "*.png")):
            shutil.copy(pngfile, dst_dir)



        except:
            continue



			
			
			

def candle_score(lst_0,lst_1,lst_2):    
    
    O_0,H_0,L_0,C_0=lst_0[0],lst_0[1],lst_0[2],lst_0[3]
    O_1,H_1,L_1,C_1=lst_1[0],lst_1[1],lst_1[2],lst_1[3]
    O_2,H_2,L_2,C_2=lst_2[0],lst_2[1],lst_2[2],lst_2[3]
    
    DojiSize = 0.1
    
    doji=(abs(O_0 - C_0) <= (H_0 - L_0) * DojiSize)
    
    hammer=(((H_0 - L_0)>3*(O_0 -C_0)) &  ((C_0 - L_0)/(.001 + H_0 - L_0) > 0.6) & ((O_0 - L_0)/(.001 + H_0 - L_0) > 0.6))
    
    inverted_hammer=(((H_0 - L_0)>3*(O_0 -C_0)) &  ((H_0 - C_0)/(.001 + H_0 - L_0) > 0.6) & ((H_0 - O_0)/(.001 + H_0 - L_0) > 0.6))
    
    bullish_reversal= (O_2 > C_2)&(O_1 > C_1)&doji
    
    bearish_reversal= (O_2 < C_2)&(O_1 < C_1)&doji
    
    evening_star=(C_2 > O_2) & (min(O_1, C_1) > C_2) & (O_0 < min(O_1, C_1)) & (C_0 < O_0 )
    
    morning_star=(C_2 < O_2) & (min(O_1, C_1) < C_2) & (O_0 > min(O_1, C_1)) & (C_0 > O_0 )
    
    shooting_Star_bearish=(O_1 < C_1) & (O_0 > C_1) & ((H_0 - max(O_0, C_0)) >= abs(O_0 - C_0) * 3) & ((min(C_0, O_0) - L_0 )<= abs(O_0 - C_0)) & inverted_hammer
    
    shooting_Star_bullish=(O_1 > C_1) & (O_0 < C_1) & ((H_0 - max(O_0, C_0)) >= abs(O_0 - C_0) * 3) & ((min(C_0, O_0) - L_0 )<= abs(O_0 - C_0)) & inverted_hammer
    
    bearish_harami=(C_1 > O_1) & (O_0 > C_0) & (O_0 <= C_1) & (O_1 <= C_0) & ((O_0 - C_0) < (C_1 - O_1 ))
    
    Bullish_Harami=(O_1 > C_1) & (C_0 > O_0) & (C_0 <= O_1) & (C_1 <= O_0) & ((C_0 - O_0) < (O_1 - C_1))
    
    Bearish_Engulfing=((C_1 > O_1) & (O_0 > C_0)) & ((O_0 >= C_1) & (O_1 >= C_0)) & ((O_0 - C_0) > (C_1 - O_1 ))
    
    Bullish_Engulfing=(O_1 > C_1) & (C_0 > O_0) & (C_0 >= O_1) & (C_1 >= O_0) & ((C_0 - O_0) > (O_1 - C_1 ))
    
    Piercing_Line_bullish=(C_1 < O_1) & (C_0 > O_0) & (O_0 < L_1) & (C_0 > C_1)& (C_0>((O_1 + C_1)/2)) & (C_0 < O_1)

    Hanging_Man_bullish=(C_1 < O_1) & (O_0 < L_1) & (C_0>((O_1 + C_1)/2)) & (C_0 < O_1) & hammer

    Hanging_Man_bearish=(C_1 > O_1) & (C_0>((O_1 + C_1)/2)) & (C_0 < O_1) & hammer

    strCandle=''
    candle_score=0
    
    if doji:
        strCandle='doji'
    if evening_star:
        strCandle=strCandle+'/ '+'evening_star'
        candle_score=candle_score-1
    if morning_star:
        strCandle=strCandle+'/ '+'morning_star'
        candle_score=candle_score+1
    if shooting_Star_bearish:
        strCandle=strCandle+'/ '+'shooting_Star_bearish'
        candle_score=candle_score-1
    if shooting_Star_bullish:
        strCandle=strCandle+'/ '+'shooting_Star_bullish'
        candle_score=candle_score-1
    if    hammer:
        strCandle=strCandle+'/ '+'hammer'
    if    inverted_hammer:
        strCandle=strCandle+'/ '+'inverted_hammer'
    if    bearish_harami:
        strCandle=strCandle+'/ '+'bearish_harami'
        candle_score=candle_score-1
    if    Bullish_Harami:
        strCandle=strCandle+'/ '+'Bullish_Harami'
        candle_score=candle_score+1
    if    Bearish_Engulfing:
        strCandle=strCandle+'/ '+'Bearish_Engulfing'
        candle_score=candle_score-1
    if    bullish_reversal:
        strCandle=strCandle+'/ '+'Bullish_Engulfing'
        candle_score=candle_score+1
    if    bullish_reversal:
        strCandle=strCandle+'/ '+'bullish_reversal'
        candle_score=candle_score+1
    if    bearish_reversal:
        strCandle=strCandle+'/ '+'bearish_reversal'
        candle_score=candle_score-1
    if    Piercing_Line_bullish:
        strCandle=strCandle+'/ '+'Piercing_Line_bullish'
        candle_score=candle_score+1
    if    Hanging_Man_bearish:
        strCandle=strCandle+'/ '+'Hanging_Man_bearish'
        candle_score=candle_score-1
    if    Hanging_Man_bullish:
        strCandle=strCandle+'/ '+'Hanging_Man_bullish'
        candle_score=candle_score+1
        
    #return candle_score
    return candle_score,strCandle


def candle_df(df):
    #df_candle=first_letter_upper(df)
    df_candle=df.copy()
    df_candle['candle_score']=0
    df_candle['candle_pattern']=''


    for c in range(2,len(df_candle)):
        cscore,cpattern=0,''
        lst_2=[df_candle['Open'].iloc[c-2],df_candle['High'].iloc[c-2],df_candle['Low'].iloc[c-2],df_candle['Close'].iloc[c-2]]
        lst_1=[df_candle['Open'].iloc[c-1],df_candle['High'].iloc[c-1],df_candle['Low'].iloc[c-1],df_candle['Close'].iloc[c-1]]
        lst_0=[df_candle['Open'].iloc[c],df_candle['High'].iloc[c],df_candle['Low'].iloc[c],df_candle['Close'].iloc[c]]
        cscore,cpattern=candle_score(lst_0,lst_1,lst_2)    
        df_candle['candle_score'].iat[c]=cscore
        df_candle['candle_pattern'].iat[c]=cpattern
    
    df_candle['candle_cumsum']=df_candle['candle_score'].rolling(3).sum()
    
    return df_candle			


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
