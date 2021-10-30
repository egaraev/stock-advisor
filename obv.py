from yahoo_fin import stock_info as si
import yfinance as yf
import datetime
import time 
from datetime import timedelta, date
import os, sys
import pandas as pd
import numpy as np
from math import floor
import pymysql
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
currtime = int(round(time.time()))
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()
days=60

def main():
    print('Starting OBV module')

    obv_analyze()
	
	


def obv_analyze():
    currtime = int(round(time.time()))
    now = datetime.datetime.now()
    currenttime = now.strftime("%Y-%m-%d %H:%M")
    currentdate = now.strftime("%Y-%m-%d")
    increased_volume = []
    for symbol in symbols: #Loop trough the crypto summary
        try:
           symbol=(symbol[0])
           name=symbol_full_name(symbol, 3)
           stock = yf.Ticker(symbol)
           hist = stock.history(period="{}d".format(days))
           df = pd.DataFrame(hist)
           df = df.reset_index().rename({'index':'Date'}, axis = 'columns')
           #df  = df.dropna()
           #print (df)

           market_df = df[['Date', 'Close', 'Volume']]
           market_df.columns = ['date', 'close', 'volume']
           market_df = market_df.sort_values('date')
           #print (market_df)
           df = on_balance_volume(market_df)
           #print (df)


           new_df = df.copy()
           new_df = new_df.drop(['close', 'volume'], axis = 1)
           #print (new_df)
           new_obv = get_obv(new_df)
           #print (new_obv)
 
           buy_price, sell_price, obv_signal = implement_obv_strategy(df['close'], new_obv)


           fig, ax = plt.subplots(figsize=(16, 8))
           plt.title(symbol)
           plt.plot(df['date'], df['close'], label='Close', color='black')
           plt.plot(df['date'], buy_price, marker = '^', color = 'green', markersize = 8, label = 'BUY SIGNAL', linewidth = 0)
           plt.plot(df['date'], sell_price, marker = 'v', color = 'r', markersize = 8, label = 'SELL SIGNAL', linewidth = 0)
           plt.legend(loc='upper left')
           plt.grid()
           # Get second axis
           ax2 = ax.twinx()
           plt.plot(df['date'],  df['obv'], label='obv',color='blue')
           plt.plot(df['date'],  df['obv_ema21'], label='obv_ema21',color='red')
           ax.plot(df['date'], buy_price, marker = '^', color = 'green', markersize = 8, label = 'BUY SIGNAL', linewidth = 0)
           ax.plot(df['date'], sell_price, marker = 'v', color = 'r', markersize = 8, label = 'SELL SIGNAL', linewidth = 0)
		   
           for i in range(len(new_obv)):
               if str(new_obv['hist'][i])[0] == '-':
                  ax2.bar(new_obv['date'][i], new_obv['hist'][i], color = '#ef5350')
               else:
                  ax2.bar(new_obv['date'][i], new_obv['hist'][i], color = '#26a69a') 
				 
           plt.legend(loc='upper right')
           #plt.show()
           plt.savefig('/root/PycharmProjects/cryptobot/images/obv_results.png')
           newfilename=("{}_obv_results.png".format(symbol))
           my_path = "/root/PycharmProjects/cryptobot/images/obv_results.png"
           new_name = os.path.join(os.path.dirname(my_path), newfilename)
           os.rename(my_path, new_name)
           print (new_name)



           position = []
           for i in range(len(obv_signal)):
             if obv_signal[i] > 1:
                 position.append(0)
             else:
                 position.append(1)
        
           for i in range(len(df['close'])):
             if obv_signal[i] == 1:
                position[i] = 1
             elif obv_signal[i] == -1:
                position[i] = 0
             else:
                position[i] = position[i-1]

		   
           obv = new_obv['obv']
           signal = new_obv['obv_ema21']
           close_price = df['close']
           obv_signal = pd.DataFrame(obv_signal).rename(columns = {0:'obv_signal'}).set_index(df.index)
           position = pd.DataFrame(position).rename(columns = {0:'obv_position'}).set_index(df.index)

           frames = [close_price, obv, signal, obv_signal, position]
           strategy = pd.concat(frames, join = 'inner', axis = 1)

   
           row_ix = strategy.shape[0]-strategy.ne(0).values[::-1].argmax(0)-1
           first_max = strategy.values[row_ix, range(strategy.shape[1])]
           out = pd.DataFrame([first_max], columns=strategy.columns)

           last_obv_signal = int(out['obv_signal'])
           print (last_obv_signal)



           obv_signal= strategy.iloc[-1]
           obv_signal = int(obv_signal['obv_signal'])
           if obv_signal == 0:
              print ("OBV is 0, nothing to do")
           else:
              if obv_signal == 1:
                 signal = "Buy"
              else:
                 signal = "Sell"
              try:
                  db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                  cursor = db.cursor()
                  cursor.execute("update symbols set obv_signal='%s'  where symbol='%s'" % (signal, symbol))
                  cursor.execute("update history set obv_signal='%s'  where symbol='%s' and date='%s'" % (signal, symbol, currentdate))
                  db.commit()
              except pymysql.Error as e:
                  print ("Error %d: %s" % (e.args[0], e.args[1]))
                  sys.exit(1)
              finally:
                  db.close()



           if last_obv_signal == 1:
                 signal = "Buy"
           else:
                 signal = "Sell"
           try:
                  db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                  cursor = db.cursor()
                  cursor.execute("update symbols set obv_signal='%s'  where symbol='%s'" % (signal, symbol))
                  db.commit()
           except pymysql.Error as e:
                  print ("Error %d: %s" % (e.args[0], e.args[1]))
                  sys.exit(1)
           finally:
                  db.close()



		  


        except:
            continue
    # print (increased_volume)	




def on_balance_volume(data, close_col='close', vol_col='volume', trend_periods=21):
    
    data_tmp = data.copy()
    counter = 0
  
    for index, row in data_tmp.iterrows():
        if counter > 0:
            last_obv = data_tmp.at[index - 1, 'obv']
            if row[close_col] > data_tmp.at[index - 1, close_col]:
                current_obv = last_obv + row[vol_col]
            elif row[close_col] < data_tmp.at[index - 1, close_col]:
                current_obv = last_obv - row[vol_col]
            else:
                current_obv = last_obv
        else:
            last_obv = 0
            current_obv = row[vol_col]
        counter += 1
       
        data_tmp.set_value(index, 'obv', current_obv)
    data_tmp['obv_ema' + str(trend_periods)] = data_tmp['obv'].ewm(ignore_na=False, min_periods=0, com=trend_periods, adjust=True).mean()
    
    return data_tmp


def implement_obv_strategy(prices, data):    
    buy_price = []
    sell_price = []
    obv_signal = []
    signal = 0

    for i in range(len(data)):
        if data['obv'][i] > data['obv_ema21'][i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                obv_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                obv_signal.append(0)
        elif data['obv'][i] < data['obv_ema21'][i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                obv_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                obv_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            obv_signal.append(0)
            
    return buy_price, sell_price, obv_signal







def get_obv(data):    
    data_tmp = data.copy()
    data_tmp['hist'] = data_tmp['obv'] - data_tmp['obv_ema21'] 
    return data_tmp












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