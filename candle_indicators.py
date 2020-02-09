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
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


###
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()
days=30

def main():
    print('Starting candle patterns module')

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
          #print (df)
       
          buy_df = df.copy() 
          candle_scored_buy= buy_df[(buy_df['candle_score'] > 0)]
          #print (symbol, candle_scored_buy)
          candle_scored_sell= df[(df['candle_score'] < 0)]		  
          labels_buy=(candle_scored_buy['candle_pattern'].tolist())
          labels_sell=(candle_scored_sell['candle_pattern'].tolist())		 
		     
          #print (ohlc_df)
         # Converting dates column to float values
          ohlc_df['Date'] = ohlc_df['Date'].map(mdates.date2num)
          legend_elements = [Line2D([0], [0], marker="^", color='w', label='B_R -> Bullish_Reversal', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='T_w_s -> Three_white_soldiers', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='T_b -> Tweezer_Bottom', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='M_S -> Morning_Star', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='BU_HR -> Bullish_Harami', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='BU_R -> Bullish_Reversal', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='Bu_E -> Bullish_Engulfing', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='P_L -> Piercing_Line_bullish', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='H_M_Bu -> Hanging_Man_bullish', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="^", color='w', label='P_L -> Piercing_Line_bullish', markerfacecolor='g', markersize=15), Line2D([0], [0], marker="v", color='r', label='T_b_c -> Three_black_crows', markersize=15), Line2D([0], [0], marker="v", color='r', label='T_b_g -> Two_black_gapping', markersize=15), Line2D([0], [0], marker="v", color='r', label='T_t -> Tweezer_Top', markersize=15), Line2D([0], [0], marker="v", color='r', label='E_S -> Evening_Star', markersize=15), Line2D([0], [0], marker="v", color='r', label='BE_HR -> Bearish_Harami', markersize=15), Line2D([0], [0], marker="v", color='r', label='BE_R -> Bearish_Reversal', markersize=15), Line2D([0], [0], marker="v", color='r', label='SS_BE -> Shooting_Star_Bearish', markersize=15), Line2D([0], [0], marker="v", color='r', label='Be_E -> Bearish_Engulfing', markersize=15), Line2D([0], [0], marker="v", color='r', label='H_M_Be -> Hanging_Man_bearish', markersize=15), Line2D([0], [0], marker="v", color='r', label='SS_BU -> Shooting_Star_Bullish', markersize=15)]		  
		  
          fig, ax = plt.subplots(figsize=(20, 15))
          ax.legend(handles=legend_elements, loc='upper left')
          # Converts raw mdate numbers to dates
          ax.xaxis_date()
          plt.xlabel("Date")	  
          # Making candlestick plot
          candlestick_ohlc(ax, ohlc_df.values, width = 0.8, colorup = 'g', colordown = 'r', alpha = 0.8)
          plt.ylabel("Price")
          plt.title(name) 	  
          ax2 = ax.twinx()
		  
		  
          candle_scored_buy['Date'] = ohlc_df['Date']
          x=candle_scored_buy['Date'].tolist()
          y=candle_scored_buy['candle_score'].tolist()
          n = labels_buy
      
          #fig, ax2 = plt.subplots()
          ax2.axhline(y=2)
          ax2.plot([x], [2], marker='o', markersize=1)
          ax2.scatter(x, y, c='g', marker="^", s=120)

          for i, txt in enumerate(n):
            ax2.annotate(txt, (x[i], y[i]))


          x1=candle_scored_sell['Date'].tolist()
          y1=candle_scored_sell['candle_score'].tolist()
          n1 = labels_sell
      
          #fig, ax2 = plt.subplots()
          ax2.scatter(x1, y1, c='r', marker="v", s=120)

          for a, txt1 in enumerate(n1):
            ax2.annotate(txt1, (x1[a], y1[a]))	
          
          ax2.axhline(y=-2)	

		  
		

		  	  
## working config		  
          #ax2.plot(x, y,  '^', markersize=15)
          #ax2.plot(candle_scored_sell['Date'], candle_scored_sell['candle_score'], 'v', markersize=15)
##working config
		  
          plt.gcf().autofmt_xdate()   # Beautify the x-labels
          plt.autoscale(tight=True)
          plt.grid()
          ax.grid(True)
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


		
			
			

def candle_score(lst_0,lst_1,lst_2,lst_3):    
    
    O_0,H_0,L_0,C_0=lst_0[0],lst_0[1],lst_0[2],lst_0[3]  #current
    O_1,H_1,L_1,C_1=lst_1[0],lst_1[1],lst_1[2],lst_1[3]  #previous
    O_2,H_2,L_2,C_2=lst_2[0],lst_2[1],lst_2[2],lst_2[3]  #previous2
    O_3,H_3,L_3,C_3=lst_3[0],lst_3[1],lst_3[2],lst_3[3]  #previous3
    
    DojiSize = 0.1

# UP trend: (C_2>C_3)
# Green candles before: (C_3 > O_3) & (C_2 > O_2)
#DOWN trend: (C_2<C_3)
# Red candles before: (C_3 < O_3) & (C_2 < O_2)
    
    doji=(abs(O_0 - C_0) <= (H_0 - L_0) * DojiSize)	
    Hammer=(((H_0 - L_0)>3*(O_0 -C_0)) &  ((C_0 - L_0)/(.001 + H_0 - L_0) > 0.6) & ((O_0 - L_0)/(.001 + H_0 - L_0) > 0.6))
    Hammer_Bullish=(((H_0 - L_0)>3*(C_0 -O_0)) &  ((O_0 - L_0)/(.001 + H_0 - L_0) > 0.6) & ((C_0 - L_0)/(.001 + H_0 - L_0) > 0.6))
	
    Inverted_Hammer=(((H_0 - L_0)>3*(O_0 -C_0)) &  ((H_0 - C_0)/(.001 + H_0 - L_0) > 0.6) & ((H_0 - O_0)/(.001 + H_0 - L_0) > 0.6))
    Inverted_Hammer_Bullish=(((H_0 - L_0)>3*(C_0 -O_0)) &  ((H_0 - O_0)/(.001 + H_0 - L_0) > 0.6) & ((H_0 - C_0)/(.001 + H_0 - L_0) > 0.6))    
    
    Bullish_Reversal = (O_2 > C_2)&(O_1 > C_1)&doji
    Bearish_Reversal = (O_2 < C_2)&(O_1 < C_1)&doji
    
    Evening_Star= (C_3 > O_3) & (C_2 > O_2) & (C_1 < O_1) & (O_1 > C_2) & (O_0 <O_1) & (C_0 < O_0 ) & ((C_2-O_2)>(O_1-C_1)) & ((O_0-C_0)>(O_1-C_1))

    Morning_Star= (C_3 < O_3) & (C_2 < O_2) & (C_1 > O_1) & (O_1 < C_2) & (O_0 > O_1) & (C_0 > O_0 )	 & ((O_2- C_2)>(C_1 - O_1)) & ((C_0-O_0)>(C_1-O_1))
	

    Shooting_Star_Bearish=(O_1 < C_1) & (O_0 > C_1) & ((H_0 - max(O_0, C_0)) >= abs(O_0 - C_0) * 3) & ((min(C_0, O_0) - L_0 )<= abs(O_0 - C_0)) & Inverted_Hammer
    
    Shooting_Star_Bullish=(O_1 > C_1) & (O_0 < C_1) & ((H_0 - max(O_0, C_0)) >= abs(O_0 - C_0) * 3) & ((min(C_0, O_0) - L_0 )<= abs(O_0 - C_0)) & Inverted_Hammer	
    
    Bearish_Harami =  (O_2 < C_2)&  (C_2<C_1)&  (C_1 > O_1) & (O_0 > C_0) & (O_0 <= C_1) & (O_1 < C_0) & ((O_0 - C_0) < (C_1 - O_1)) & ((C_1 - O_1)/(O_0 - C_0)>=2)
	
    Bullish_Harami =  (C_2 < O_2)&  (C_1<C_2)&  (O_1 > C_1) & (C_0 > O_0) & (C_0 <= O_1) & (C_1 < O_0) & ((C_0 - O_0) < (O_1 - C_1)) & ((O_1 - C_1)/(C_0 - O_0)>=2)	
	
    Bearish_Engulfing=((C_1 > O_1) & (O_0 > C_0)) & ((O_0 > C_1) & (O_1 > C_0)) & ((O_0 - C_0) > (C_1 - O_1 ))  & (C_2 > O_2)
    
    Bullish_Engulfing=(O_1 > C_1) & (C_0 > O_0) & (C_0 > O_1) & (C_1 > O_0) & ((C_0 - O_0) > (O_1 - C_1 ))  & (C_2 < O_2)	
	
    Piercing_Line_bullish=(C_1 < O_1) & (C_0 > O_0) & (O_0 < L_1) & (C_0 > C_1)& (C_0>((O_1 + C_1)/2)) & (C_0 < O_1)
	
    Hanging_Man_bullish=(C_1 < O_1) & (O_0 < L_1) & (C_0>((O_1 + C_1)/2)) & (C_0 < O_1) & Hammer

    Hanging_Man_bearish=(C_1 > O_1) & (C_0>((O_1 + C_1)/2)) & (C_0 < O_1) & Hammer
	
    Tweezer_Top = (C_3 > O_3) & (C_2 > O_2) & (C_1>O_1) & (C_0<O_0) & (C_1==O_0)
	
    Tweezer_Bottom=(C_3 < O_3) & (C_2 < O_2) & (C_1<O_1) & (C_0>O_0) & (O_1==C_0)

    Two_black_gapping = (C_3 > O_3) & (C_2 > O_2) & (C_1<O_1) & (C_0<O_0) & (L_1>H_0)	

    Three_white_soldiers=(C_3 < O_3) & (C_2 > O_2) & (C_1 > O_1) & (C_0 > O_0)  & (O_0>O_1) &(O_1>O_2) & (L_3<L_2)

    Three_black_crows=(C_3 > O_3) & (C_2 < O_2) & (C_1 < O_1) & (C_0 < O_0)	& (O_0<O_1) &(O_1<O_2) & (L_3>L_2)

    strCandle=''
    candle_score=0
    
#    if doji:
#        strCandle='doji'
    if    Three_black_crows:
        strCandle=strCandle+'/ '+'T_b_c'
        candle_score=candle_score-1	
    if    Three_white_soldiers:
        strCandle=strCandle+'/ '+'T_w_s'
        candle_score=candle_score+1			
    if    Two_black_gapping:
        strCandle=strCandle+'/ '+'T_b_g'
        candle_score=candle_score-1		
    if    Tweezer_Top:
        strCandle=strCandle+'/ '+'T_t'
        candle_score=candle_score-1
    if    Tweezer_Bottom:
        strCandle=strCandle+'/ '+'T_b'
        candle_score=candle_score+1		
    if    Evening_Star:
        strCandle=strCandle+'/ '+'E_S'
        candle_score=candle_score-1	
    if    Morning_Star:
        strCandle=strCandle+'/ '+'M_S'
        candle_score=candle_score+1
		
    if    Bullish_Harami:
        strCandle=strCandle+'/ '+'BU_HR'
        candle_score=candle_score+1
    if    Bearish_Harami:
        strCandle=strCandle+'/ '+'BE_HR'
        candle_score=candle_score-1	
    if    Bullish_Reversal:
        strCandle=strCandle+'/ '+'BU_R'
        candle_score=candle_score+1
    if    Bearish_Reversal:
        strCandle=strCandle+'/ '+'BE_R'
        candle_score=candle_score-1		
#    if    Hammer:
#        strCandle=strCandle+'/ '+'H'
#    if    Inverted_Hammer:
#        strCandle=strCandle+'/ '+'I_H'
    if Shooting_Star_Bearish:
        strCandle=strCandle+'/ '+'SS_BE'
        candle_score=candle_score-1
    if Shooting_Star_Bullish:
        strCandle=strCandle+'/ '+'SS_BU'
        candle_score=candle_score-1		
    if    Bearish_Engulfing:
        strCandle=strCandle+'/ '+'Be_E'
        candle_score=candle_score-1
    if    Bullish_Engulfing:
        strCandle=strCandle+'/ '+'Bu_E'
        candle_score=candle_score+1
    if    Piercing_Line_bullish:
        strCandle=strCandle+'/ '+'P_L'
        candle_score=candle_score+1
    if    Hanging_Man_bearish:
        strCandle=strCandle+'/ '+'H_M_Be'
        candle_score=candle_score-1
    if    Hanging_Man_bullish:
        strCandle=strCandle+'/ '+'H_M_Bu'
        candle_score=candle_score+1



		
        
    #return candle_score
    return candle_score,strCandle


def candle_df(df):

    df_candle=df.copy()
    df_candle['candle_score']=0
    df_candle['candle_pattern']=''


    for c in range(2,len(df_candle)):
        cscore,cpattern=0,''
        lst_3=[df_candle['Open'].iloc[c-3],df_candle['High'].iloc[c-3],df_candle['Low'].iloc[c-3],df_candle['Close'].iloc[c-3]]
        lst_2=[df_candle['Open'].iloc[c-2],df_candle['High'].iloc[c-2],df_candle['Low'].iloc[c-2],df_candle['Close'].iloc[c-2]]
        lst_1=[df_candle['Open'].iloc[c-1],df_candle['High'].iloc[c-1],df_candle['Low'].iloc[c-1],df_candle['Close'].iloc[c-1]]
        lst_0=[df_candle['Open'].iloc[c],df_candle['High'].iloc[c],df_candle['Low'].iloc[c],df_candle['Close'].iloc[c]]
        cscore,cpattern=candle_score(lst_0,lst_1,lst_2,lst_3)    
        df_candle['candle_score'].iat[c]=cscore
        df_candle['candle_pattern'].iat[c]=cpattern
    
    #df_candle['candle_cumsum']=df_candle['candle_score'].rolling(3).sum()
    
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
