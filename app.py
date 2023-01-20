

from flask import Flask, render_template, jsonify
import yfinance as yf
import talib
import csv
import requests
import pandas as pd

app = Flask(__name__)
option = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
@app.route('/crossing-stocks/<int:days>', methods=['GET'])

def crossing_stocks(days):
    # Define a list to store the crossing stocks
    crossing_stocks = []
    listStockCodes = []
    csvfile = "tickers.csv"
    
    #res = requests.get(option)
    f = open(csvfile)
    csvreader = csv.reader(f)
    header = next(csvreader)
    print(header)

    for row in csvreader:
      listStockCodes.append(row)
      
    f.close()
    print(listStockCodes)
    # Download historical data for all stocks in the Nifty 500
    for stock in listStockCodes:
      try:      
        result_df = yf.download(stock, start="2022-01-01", end="2023-01-20", progress=True)        
    
        # Calculate the 200-day MA
        result_df["200-day MA"] = talib.MA(result_df["Close"], timeperiod=200)

        # Calculate the 10-day MA
        result_df["10-day MA"] = talib.MA(result_df["Close"], timeperiod=10)

        # Calculate the 20-day MA
        result_df["20-day MA"] = talib.MA(result_df["Close"], timeperiod=20)

        # Get the last 'days' rows of data
        result_df = result_df.tail(days)

        # Check if the stock has crossed the 200-day MA in the last 'days' days
        if (result_df["Close"].iloc[-1] > result_df["200-day MA"].iloc[-1]) & (result_df["Close"].iloc[0] <= result_df["200-day MA"].iloc[0]):

          # Check if the stock is currently above the 10-day MA or 20-day MA
          if (result_df["Close"].iloc[-1] > result_df["10-day MA"].iloc[-1]) | (result_df["Close"].iloc[-1] > result_df["20-day MA"].iloc[-1]):

            # Add the stock to the list of crossing stocks
            name = stock[0].split('.')[0]
            crossing_stocks.append(name)
      except Exception as e:
        print(e)
        pass
       
    return render_template('crossing_stocks.html', crossing_stocks=crossing_stocks)