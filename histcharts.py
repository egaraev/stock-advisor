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
          cursor.execute("SELECT date, twitter_polarity, twitter_score, news_score, price, predicted_price FROM history WHERE symbol='%s'" % symbol)
          data=cursor.fetchall()

          df = pd.DataFrame(data)
          df.columns = ['date', 'twitter_polarity', 'twitter_score', 'news_score', 'price', 'predicted_price']

          rc('mathtext', default='regular')

          fig = plt.figure(figsize=(15,10))
          plt.title(name)
          ax = fig.add_subplot(111)

          lns1 = ax.plot(df['date'], df['price'], '-', linewidth = 3, label = 'Price')
          lns2 = ax.plot(df['date'], df['predicted_price'], '-', c='blue', linestyle = '--', linewidth = 3, label = 'Prediction')
          ax2 = ax.twinx()
          lns3 = ax2.plot(df['date'], df['news_score'], '-r', c='green', linewidth = 3, label = 'News score')
          lns4 = ax2.plot(df['date'], df['twitter_score'], '', c='red', linewidth = 3, label = 'Twitter score')
          lns5 = ax2.plot(df['date'], df['twitter_polarity'], '-', c='orange', linewidth = 3, label = 'Twitter polarity')

          # added these three lines
          lns = lns1+lns2+lns3+lns4+lns5
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
