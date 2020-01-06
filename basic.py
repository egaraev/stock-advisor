import yfinance as yf
import pymysql
import pandas as pd
from yahoo_fin import stock_info as si
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
          print (symbol)
          stock = yf.Ticker(symbol)
          print (si.get_live_price(symbol))
          
#          print (si.get_quote_table(symbol , dict_result = True))
          hist = stock.history(period="1d")
          df = pd.DataFrame(hist)
          print (df['Open'].tolist())
          print (df['Close'].tolist())
          print (df['Low'].tolist())
          print (df['High'].tolist())


        except:
            continue




if __name__ == "__main__":
    main()
