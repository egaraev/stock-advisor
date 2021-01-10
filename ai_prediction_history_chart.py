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
    print('Starting historical charts  module')


    SL()


def SL():
    for symbol in symbols: #Loop trough the stock summary
        try:
          symbol=(symbol[0])
          name=symbol_full_name(symbol, 3)
          print (symbol)
          db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
          cursor = db.cursor()
          cursor.execute("SELECT date, price, predicted_price FROM history WHERE symbol='%s' ORDER BY date DESC LIMIT 300" % symbol)
          data=cursor.fetchall()

          df = pd.DataFrame(data)

		  
		  
		  
          #df.set_index('date')
          df.columns = ['date',  'price', 'predicted_price']
		  
          df['date_index'] = df['date']
          df['date_index'] = pd.to_datetime(df['date_index'])
          df= df.set_index('date_index')
          df=df.sort_index()
          

          rc('mathtext', default='regular')

          fig = plt.figure(figsize=(15,10))
          plt.title(name)
          ax = fig.add_subplot(111)
          
          series1=(df['price'])
          s1mask = np.isfinite(series1)
          series2=(df['predicted_price'])
          s2mask = np.isfinite(series2)
  

          lns1 = ax.plot(df['date'][s1mask], series1[s1mask], linewidth = 3, label = 'Price')
          lns2 = ax.plot(df['date'][s2mask], series2[s2mask], c='blue', linestyle = '--', linewidth = 3, label = 'Prediction')

		  

          # added these three lines
          lns = lns1+lns2
          labs = [l.get_label() for l in lns]
          ax.legend(lns, labs, loc=0)
          ax.set_xticklabels([])
  #        ax.grid()
  #        ax.set_xlabel("Date")
  #        ax.set_ylabel(r"Stock Price")
  #        plt.gcf().autofmt_xdate()   # Beautify the x-labels


          plt.savefig('/root/PycharmProjects/stock-advisor/images/ai_history.png')
		  
          newfilename=("{}_ai_history.png".format(symbol))
          my_path = "/root/PycharmProjects/stock-advisor/images/ai_history.png"
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
