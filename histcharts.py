import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc
import io, base64, os, json, re, sys 
import glob
import shutil
import time
import pymysql
import matplotlib.dates as mdates
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()

def main():
    print('Starting stock loop  module')


    SL()


def SL():
    for symbol in symbols: #Loop trough the stock summary
        try:
          symbol=(symbol[0])
          name=symbol_full_name(symbol, 3)
          print (symbol)
          db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
          cursor = db.cursor()
          cursor.execute("SELECT date, twitter_polarity, twitter_score, news_score, price, predicted_price, positive_tweets, negative_tweets FROM history WHERE symbol='%s'" % symbol)
          data=cursor.fetchall()

          df = pd.DataFrame(data)

		  
		  
		  
          #df.set_index('date')
          df.columns = ['date', 'twitter_polarity', 'twitter_score', 'news_score', 'price', 'predicted_price', 'positive_tweets', 'negative_tweets']
		  
          df['date_index'] = df['date']
          #df['date_index'] = pd.to_datetime(df['date_index'])
          #df['date_index'] = pd.to_datetime(df['date_index'], infer_datetime_format=True)
          df['date_index'] = pd.to_datetime(df['date_index'])
          df= df.set_index('date_index')
          df=df.sort_index()
          
          #df.info()
          print (df)

          rc('mathtext', default='regular')

          fig = plt.figure(figsize=(15,10))
          plt.title(name)
          ax = fig.add_subplot(111)
          
          #s1mask = np.isfinite(series1)
          series1=(df['price'])
          s1mask = np.isfinite(series1)
          series2=(df['predicted_price'])
          s2mask = np.isfinite(series2)
		  
          series3=(df['positive_tweets'])
          s3mask = np.isfinite(series3)
          series4=(df['negative_tweets'])
          s4mask = np.isfinite(series4)
		  
          series5=(df['news_score'])
          s5mask = np.isfinite(series5)
          series6=(df['twitter_score'])
          s6mask = np.isfinite(series6)		  
          series7=(df['twitter_polarity'])
          s7mask = np.isfinite(series7)	

		  

          lns1 = ax.plot(df['date'][s1mask], series1[s1mask], '-', linewidth = 3, label = 'Price')
          lns2 = ax.plot(df['date'][s2mask], series2[s2mask], '-', c='blue', linestyle = '--', linewidth = 3, label = 'Prediction')
          lns3 = ax.plot(df['date'][s3mask], series3[s3mask], '-', c='magenta', linewidth = 3, label = 'Positive tweets')
          lns4 = ax.plot(df['date'][s4mask], series4[s4mask], '-', c='sienna', linewidth = 3, label = 'Negative tweets')
          ax2 = ax.twinx()
          lns5 = ax2.plot(df['date'][s5mask], series5[s5mask], '-r', c='green', linewidth = 3, label = 'News score')
          lns6 = ax2.plot(df['date'][s6mask], series6[s6mask], '', c='red', linewidth = 3, label = 'Twitter score')
          lns7 = ax2.plot(df['date'][s7mask], series7[s7mask], '-', c='orange', linewidth = 3, label = 'Twitter polarity')

          # added these three lines
          lns = lns1+lns2+lns3+lns4+lns5+lns6+lns7
          labs = [l.get_label() for l in lns]
          ax.legend(lns, labs, loc=0)

          ax.grid()
          ax.set_xlabel("Date")
          ax.set_ylabel(r"Stock Price")
          ax2.set_ylabel(r"Score")
          ax2.set_ylim(-1, 4)
#          ax.set_ylim(-20,100)


          plt.savefig('/root/PycharmProjects/stock-advisor/images/history.png')
		  
          newfilename=("{}_history.png".format(symbol))
          my_path = "/root/PycharmProjects/stock-advisor/images/history.png"
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