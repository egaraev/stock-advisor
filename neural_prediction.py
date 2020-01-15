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
import requests
from bs4 import BeautifulSoup
import json
import urllib
from urllib.request import urlopen
###
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()


# Window size or the sequence length
N_STEPS = 100
# Lookup step, 1 is the next day
LOOKUP_STEP = 90
# test ratio size, 0.2 is 20%
TEST_SIZE = 0.2
# features to use
FEATURE_COLUMNS = ["adjclose", "volume", "open", "high", "low"]
# date now
date_now = time.strftime("%Y-%m-%d")
### model parameters
N_LAYERS = 3
# LSTM cell
CELL = LSTM
# 256 LSTM neurons
UNITS = 256
# 40% dropout
DROPOUT = 0.4
### training parameters
# mean squared error loss
LOSS = "mse"
OPTIMIZER = "rmsprop"
BATCH_SIZE = 64
EPOCHS = 300 



def main():
    print('Starting neural-analyse module')

    neural()


def neural():
    for symbol in symbols: #Loop trough the stock summary
        try:
          symbol=(symbol[0])
          name=symbol_full_name(symbol, 3)
        # create these folders if they does not exist
          if not os.path.isdir("/root/PycharmProjects/stock-advisor/results"):
             os.mkdir("/root/PycharmProjects/stock-advisor/results")
          if not os.path.isdir("/root/PycharmProjects/stock-advisor/logs"):
             os.mkdir("/root/PycharmProjects/stock-advisor/logs")
          if not os.path.isdir("/root/PycharmProjects/stock-advisor/data"):
             os.mkdir("/root/PycharmProjects/stock-advisor/data")

          ticker = symbol
          ticker_data_filename = os.path.join("data", f"{ticker}_{date_now}.csv")
          # model name to save
          model_name = f"{date_now}_{ticker}-{LOSS}-{CELL.__name__}-seq-{N_STEPS}-step-{LOOKUP_STEP}-layers-{N_LAYERS}-units-{UNITS}"




#          # load the CSV file from disk (dataset) if it already exists (without downloading)
          if os.path.isfile(ticker_data_filename):
              ticker = pd.read_csv(ticker_data_filename)

          # load the data
          data = load_data(ticker, N_STEPS, lookup_step=LOOKUP_STEP, test_size=TEST_SIZE, feature_columns=FEATURE_COLUMNS)

          if not os.path.isfile(ticker_data_filename):
          # save the CSV file (dataset)
             data["df"].to_csv(ticker_data_filename)

          # construct the model
          model = create_model(N_STEPS, loss=LOSS, units=UNITS, cell=CELL, n_layers=N_LAYERS, dropout=DROPOUT, optimizer=OPTIMIZER)

          # some tensorflow callbacks
          checkpointer = ModelCheckpoint(os.path.join("results", model_name), save_weights_only=True, save_best_only=True, verbose=1)
          tensorboard = TensorBoard(log_dir=os.path.join("logs", model_name))

          history = model.fit(data["X_train"], data["y_train"],
                    batch_size=BATCH_SIZE,
                    epochs=EPOCHS,
                    validation_data=(data["X_test"], data["y_test"]),
                    callbacks=[checkpointer, tensorboard],
                    verbose=1)

          model.save(os.path.join("results", model_name) + ".h5")
          print ("Model trained")

          # load the data
          data = load_data(ticker, N_STEPS, lookup_step=LOOKUP_STEP, test_size=TEST_SIZE, feature_columns=FEATURE_COLUMNS, shuffle=False)

          # construct the model
          model = create_model(N_STEPS, loss=LOSS, units=UNITS, cell=CELL, n_layers=N_LAYERS, dropout=DROPOUT, optimizer=OPTIMIZER)

          model_path = os.path.join("results", model_name) + ".h5"
          model.load_weights(model_path)

          # evaluate the model
          mse, mae = model.evaluate(data["X_test"], data["y_test"])
          # calculate the mean absolute error (inverse scaling)
          mean_absolute_error = data["column_scaler"]["adjclose"].inverse_transform(mae.reshape(1, -1))[0][0]
          print("Mean Absolute Error:", mean_absolute_error)
          # predict the future price
          future_price = predict(model, data)
          print (future_price)
          try:
              db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
              cursor = db.cursor()
              cursor.execute("update symbols set predicted_price='%s'  where symbol='%s'" % (future_price, symbol)) 
              db.commit()
          except pymysql.Error as e:
              print ("Error %d: %s" % (e.args[0], e.args[1]))
              sys.exit(1)
          finally:
              db.close()

          print(f"Future price after {LOOKUP_STEP} days is {future_price:.2f}$")
          print("Accuracy Score:", get_accuracy(model, data))
          plot_graph(model, data, name)
          newfilename=("{}_result.png".format(symbol))
          my_path = "/root/PycharmProjects/stock-advisor/images/results.png"
          new_name = os.path.join(os.path.dirname(my_path), newfilename)
          os.rename(my_path, new_name)
          src_dir = "/root/PycharmProjects/stock-advisor/images/"
          dst_dir = "/var/www/html/images/"
          for pngfile in glob.iglob(os.path.join(src_dir, "*.png")):
            shutil.copy(pngfile, dst_dir)

          files = glob.glob('/root/PycharmProjects/stock-advisor/results/*')
          for f in files:
            os.remove(f)

          files2 = glob.glob('/root/PycharmProjects/stock-advisor/logs/*')
          for f in files2:
            os.remove(f)
          return symbol

        except:
            continue





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
#    plt.show()


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


def create_model(input_length, units=256, cell=LSTM, n_layers=2, dropout=0.3, loss="mean_absolute_error", optimizer="rmsprop"):
    model = Sequential()
    for i in range(n_layers):
        if i == 0:
            # first layer
            model.add(cell(units, return_sequences=True, input_shape=(None, input_length)))
        elif i == n_layers - 1:
            # last layer
            model.add(cell(units, return_sequences=False))
        else:
            # hidden layers
            model.add(cell(units, return_sequences=True))
        # add dropout after each layer
        model.add(Dropout(dropout))
    
    model.add(Dense(1, activation="linear"))
    model.compile(loss=loss, metrics=["mean_absolute_error"], optimizer=optimizer)

    return model




def load_data(ticker, n_steps=50, scale=True, shuffle=True, lookup_step=1, test_size=0.2, feature_columns=['adjclose', 'volume', 'open', 'high', 'low']):
    """
    Loads data from Yahoo Finance source, as well as scaling, shuffling, normalizing and splitting.
    Params:
        ticker (str/pd.DataFrame): the ticker you want to load, examples include AAPL, TESL, etc.
        n_steps (int): the historical sequence length (i.e window size) used to predict, default is 50
        scale (bool): whether to scale prices from 0 to 1, default is True
        shuffle (bool): whether to shuffle the data, default is True
        lookup_step (int): the future lookup step to predict, default is 1 (e.g next day)
        test_size (float): ratio for test data, default is 0.2 (20% testing data)
        feature_columns (list): the list of features to use to feed into the model, default is everything grabbed from yahoo_fin
    """
    # see if ticker is already a loaded stock from yahoo finance
    if isinstance(ticker, str):
        # load it from yahoo_fin library
        df = si.get_data(ticker)
    elif isinstance(ticker, pd.DataFrame):
        # already loaded, use it directly
        df = ticker
    else:
        raise TypeError("ticker can be either a str or a `pd.DataFrame` instances")

    # this will contain all the elements we want to return from this function
    result = {}
    # we will also return the original dataframe itself
    result['df'] = df.copy()

    # make sure that the passed feature_columns exist in the dataframe
    for col in feature_columns:
        assert col in df.columns

    if scale:
        column_scaler = {}
        # scale the data (prices) from 0 to 1
        for column in feature_columns:
            scaler = preprocessing.MinMaxScaler()
            df[column] = scaler.fit_transform(np.expand_dims(df[column].values, axis=1))
            column_scaler[column] = scaler

        # add the MinMaxScaler instances to the result returned
        result["column_scaler"] = column_scaler

    # add the target column (label) by shifting by `lookup_step`
    df['future'] = df['adjclose'].shift(-lookup_step)

    # last `lookup_step` columns contains NaN in future column
    # get them before droping NaNs
    last_sequence = np.array(df[feature_columns].tail(lookup_step))
    
    # drop NaNs
    df.dropna(inplace=True)

    sequence_data = []
    sequences = deque(maxlen=n_steps)

    for entry, target in zip(df[feature_columns].values, df['future'].values):
        sequences.append(entry)
        if len(sequences) == n_steps:
            sequence_data.append([np.array(sequences), target])

    # get the last sequence by appending the last `n_step` sequence with `lookup_step` sequence
    # for instance, if n_steps=50 and lookup_step=10, last_sequence should be of 59 (that is 50+10-1) length
    # this last_sequence will be used to predict in future dates that are not available in the dataset
    last_sequence = list(sequences) + list(last_sequence)
    # shift the last sequence by -1
    last_sequence = np.array(pd.DataFrame(last_sequence).shift(-1).dropna())
    # add to result
    result['last_sequence'] = last_sequence
    
    # construct the X's and y's
    X, y = [], []
    for seq, target in sequence_data:
        X.append(seq)
        y.append(target)

    # convert to numpy arrays
    X = np.array(X)
    y = np.array(y)

    # reshape X to fit the neural network
    X = X.reshape((X.shape[0], X.shape[2], X.shape[1]))
    
    # split the dataset
    result["X_train"], result["X_test"], result["y_train"], result["y_test"] = train_test_split(X, y, test_size=test_size, shuffle=shuffle)
    # return the result
    return result




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
