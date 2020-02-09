from parameters import *
from stock_prediction import create_model, load_data
from tensorflow.keras.layers import LSTM
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
import os
import pandas as pd
from os import path
import glob
import shutil
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
###
db = pymysql.connect("localhost", "stockuser", "123456", "stock_advisor")
cursor = db.cursor()
cursor.execute("SELECT symbol FROM symbols WHERE active=1")
symbols=cursor.fetchall()





def main():
    print('Starting neural-analyse training module')

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

          print (symbol)

          ticker = symbol
          ticker_data_filename = os.path.join("/root/PycharmProjects/stock-advisor/data", f"{ticker}_{date_now}.csv")
          # model name to save
          model_name = f"{date_now}_{ticker}-{LOSS}-{CELL.__name__}-seq-{N_STEPS}-step-{LOOKUP_STEP}-layers-{N_LAYERS}-units-{UNITS}"
          fileexist=("/root/PycharmProjects/stock-advisor/results/"+ model_name+ ".h5")
          if path.exists(fileexist):
              print ("Model already trained")
          else:
              print ("Starting to train model")		 




#          # load the CSV file from disk (dataset) if it already exists (without downloading)
              if os.path.isfile(ticker_data_filename):
                  ticker = pd.read_csv(ticker_data_filename)

              print ("load the data")
              data = load_data(ticker, N_STEPS, lookup_step=LOOKUP_STEP, test_size=TEST_SIZE, feature_columns=FEATURE_COLUMNS)

              if not os.path.isfile(ticker_data_filename):
          # save the CSV file (dataset)
                 data["df"].to_csv(ticker_data_filename)

          # construct the model
              model = create_model(N_STEPS, loss=LOSS, units=UNITS, cell=CELL, n_layers=N_LAYERS, dropout=DROPOUT, optimizer=OPTIMIZER)

          # some tensorflow callbacks
              checkpointer = ModelCheckpoint(os.path.join("/root/PycharmProjects/stock-advisor/results", model_name), save_weights_only=True, save_best_only=True, verbose=1)
              tensorboard = TensorBoard(log_dir=os.path.join("/root/PycharmProjects/stock-advisor/logs", model_name))

              history = model.fit(data["X_train"], data["y_train"],
                        batch_size=BATCH_SIZE,
                        epochs=EPOCHS,
                        validation_data=(data["X_test"], data["y_test"]),
                        callbacks=[checkpointer, tensorboard],
                        verbose=1)

              model.save(os.path.join("/root/PycharmProjects/stock-advisor/results", model_name) + ".h5")
		  
              print ("Model trained")
		  
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
