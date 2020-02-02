from stock_prediction import create_model, load_data, np
from parameters import *
import os
import glob
import shutil
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from yahoo_fin import stock_info as si
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import sys
import re
import pymysql
import pandas as pd
from dateutil import parser
import warnings
warnings.filterwarnings('ignore')
import requests
import datetime
now = datetime.datetime.now()
from datetime import timedelta, date
currenttime = now.strftime("%Y-%m-%d %H:%M")
currentdate = now.strftime("%Y-%m-%d")
futuredate = date.today() + timedelta(days=7)

###
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()
#date_now = time.strftime("%Y-%m-%d")
from PIL import Image, ExifTags


def main():
    print('Starting neural-analyse prediction module')

    neural()


def neural():
    for symbol in symbols: #Loop trough the stock summary
        try:
          symbol=(symbol[0])
          name=symbol_full_name(symbol, 3)
          ticker= symbol
          print ("Now lets test the model")
          print (ticker, futuredate)
          ticker_data_filename = os.path.join("/root/PycharmProjects/stock-advisor/data", f"{ticker}_{date_now}.csv")
          print ("model name to save")
          model_name = f"{date_now}_{ticker}-{LOSS}-{CELL.__name__}-seq-{N_STEPS}-step-{LOOKUP_STEP}-layers-{N_LAYERS}-units-{UNITS}"

          print ("load the data")
          data = load_data(ticker, N_STEPS, lookup_step=LOOKUP_STEP, test_size=TEST_SIZE, feature_columns=FEATURE_COLUMNS, shuffle=False)

          # construct the model
          model = create_model(N_STEPS, loss=LOSS, units=UNITS, cell=CELL, n_layers=N_LAYERS, dropout=DROPOUT, optimizer=OPTIMIZER)

          model_path = os.path.join("/root/PycharmProjects/stock-advisor/results", model_name) + ".h5"
          model.load_weights(model_path)

          # evaluate the model
          mse, mae = model.evaluate(data["X_test"], data["y_test"])
          # calculate the mean absolute error (inverse scaling)
          mean_absolute_error = data["column_scaler"]["adjclose"].inverse_transform(mae.reshape(1, -1))[0][0]
          print("Mean Absolute Error:", mean_absolute_error)
          # predict the future price
          future_price = predict(model, data)
          print (future_price, futuredate)
          printed = (symbol, f"Future price after {LOOKUP_STEP} days is {future_price:.2f}$")
          try:
              db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
              cursor = db.cursor()
              cursor.execute("update symbols set predicted_price='%s'  where symbol='%s'" % (future_price, symbol))
              cursor.execute('insert into logs(date, entry) values("%s", "%s")', (currenttime, printed))			  
              db.commit()
          except pymysql.Error as e:
              print ("Error %d: %s" % (e.args[0], e.args[1]))
              sys.exit(1)
          finally:
              db.close()
			  
          if date_exist(symbol, currentdate) != 1:
             try:
                 db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
                 cursor = db.cursor()
                 cursor.execute('insert into history(predicted_price, date, symbol) values("%s", "%s", "%s")' % (future_price, futuredate, symbol))
                 db.commit()
             except pymysql.Error as e:
                 print ("Error %d: %s" % (e.args[0], e.args[1]))
                 sys.exit(1)
             finally:
                 db.close()
          else:
              pass			  


          print(f"Future price after {LOOKUP_STEP} days is {future_price:.2f}$")
          print("Accuracy Score:", get_accuracy(model, data))
          plot_graph(model, data, name)
          newfilename=("{}_result.png".format(symbol))
          my_path = "/root/PycharmProjects/stock-advisor/images/results.png"
          new_name = os.path.join(os.path.dirname(my_path), newfilename)
          os.rename(my_path, new_name)

          print (new_name)

          src_dir = "/root/PycharmProjects/stock-advisor/images/"
          dst_dir = "/var/www/html/images/"
          for pngfile in glob.iglob(os.path.join(src_dir, "*.png")):
            shutil.copy(pngfile, dst_dir)



        except:
            continue


					
def date_exist(symbolname, currentdate):
    db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
    cursor = db.cursor()
    symbol = symbolname
    cursor.execute("SELECT * FROM history WHERE symbol = '%s' and date='%s'" % (symbol, currentdate))
    r = cursor.fetchall()
    for row in r:
        if row[0] is not None:
            return 1

        else:
            return 0


def plot_graph(model, data, name):
    y_test = data["y_test"]
    X_test = data["X_test"]
    y_pred = model.predict(X_test)
    y_test = np.squeeze(data["column_scaler"]["adjclose"].inverse_transform(np.expand_dims(y_test, axis=0)))
    y_pred = np.squeeze(data["column_scaler"]["adjclose"].inverse_transform(y_pred))
    plt.close()
    plt.plot(y_test[-200:], c='b')
    plt.plot(y_pred[-200:], c='r')
    plt.title(name)
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.legend(["Actual Price", "Predicted Price"])
    plt.savefig('/root/PycharmProjects/stock-advisor/images/results.png')
    plt.show()


def get_accuracy(model, data):
    y_test = data["y_test"]
    X_test = data["X_test"]
    y_pred = model.predict(X_test)
    y_test = np.squeeze(data["column_scaler"]["adjclose"].inverse_transform(np.expand_dims(y_test, axis=0)))
    y_pred = np.squeeze(data["column_scaler"]["adjclose"].inverse_transform(y_pred))
    y_pred = list(map(lambda current, future: int(float(future) > float(current)), y_test[:-LOOKUP_STEP], y_pred[LOOKUP_STEP:]))
    y_test = list(map(lambda current, future: int(float(future) > float(current)), y_test[:-LOOKUP_STEP], y_test[LOOKUP_STEP:]))
    return accuracy_score(y_test, y_pred)


def predict(model, data, classification=False):
    # retrieve the last sequence from data
    last_sequence = data["last_sequence"][:N_STEPS]
    # retrieve the column scalers
    column_scaler = data["column_scaler"]
    # reshape the last sequence
    last_sequence = last_sequence.reshape((last_sequence.shape[1], last_sequence.shape[0]))
    # expand dimension
    last_sequence = np.expand_dims(last_sequence, axis=0)
    # get the prediction (scaled from 0 to 1)
    prediction = model.predict(last_sequence)
    # get the price (by inverting the scaling)
    predicted_price = column_scaler["adjclose"].inverse_transform(prediction)[0][0]
    return predicted_price


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
