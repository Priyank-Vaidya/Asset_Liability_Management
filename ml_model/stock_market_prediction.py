# -*- coding: utf-8 -*-
"""Stock_Market_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vhel8fEllXREZFWNN7LWM8rjQxe0XhWh
"""

# Commented out IPython magic to ensure Python compatibility.
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('default')
import statsmodels.tsa.arima.model as sm
from sklearn.metrics import mean_squared_error
# %matplotlib inline
from flask import Flask, request, jsonify
import os
# from db import conn

# Connect to the database

def get_historical_data(symbol):
    end = datetime.now()
    print(end.year)
    start = end - pd.DateOffset(years=5)
    data = yf.download(symbol, start=start, end=end)
    df = pd.DataFrame(data=data)
    df['Date'] = pd.date_range(end, periods=len(df))
    # df['Date'] = df.index
    df = df.set_index('Date')
    data_dir = '../data/'

# Construct the file path including the directory and file name

    file_path = os.path.join(data_dir, f'{symbol}.csv')

# Save the DataFrame as CSV to the specified file path

    if not os.path.isfile(file_path):
        # File does not exist, download it
        print(f"Downloading the {symbol} data for 3 years...")
        df.to_csv(file_path, index=False)

    # df.to_csv(f'{symbol}.csv', index=False)

    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("Downloading complete")
    
    return df

def preprocess_data(df):  
  # if 'Date' in df.columns:
  #     df['Date'] = pd.to_datetime(df['Date'])
  # else:
  #     df['Date'] = pd.to_datetime(df.index)
    #Using Exponential Moving Average for Better Prediction
  df.sort_index(inplace=True)

  df['EMA30'] = df['Close'].ewm(span=30).mean()
  # df[['Close', 'EMA30']].plot(label="APPLE", figsize = (16,8))

  print(df)

  # df.set_index('Date')
  seasonal_values = df.groupby(pd.Grouper(freq='Q')).mean(numeric_only=True)
  
  # Merge the seasonal values with the original DataFrame.
  df = df.merge(seasonal_values, on='Date', how='left')

  # Fill in the NaN values with zeros.
  df = df.fillna(0)

  print("Pre-Processing Complete")

  # data.head()
  return df

def compute_model(df):
  
  model = sm.ARIMA(df['Close_x'], order=(1, 1, 1), seasonal_order=(1,1,1,4))

 # Set the index to the 'Date' column
  # df.sort_index(inplace=True)  # Sort the index in ascending order

  # Fit the model
  print("----")
  ft = model.fit()
  print("--------")

  print("######################################")
  print("Summary of the Model")

  print(ft.summary())

  # forecast = model.forecast(steps=365)[0]
# Predict the closing value after a year
  # params = model.params.tolist()
  # print(params)
  start_date = df.index[-1]
  print(start_date)
  end_date = start_date + pd.DateOffset(days=365)
  print(end_date)

  # Generate a new index range that includes the forecast period
  forecast_index = pd.date_range(start=start_date, end=end_date, freq='D')

  print(forecast_index)

  prediction = ft.predict(start=start_date, end=end_date, dynamic=False)
  # prediction = ft.predict(start=df.index[-1], end=df.index[-1].to_datetime().apply(lambda a: a.timestamp()) + pd.Timedelta(days=365), dynamic= False )

  actual_prices = df['Close_x'][:len(prediction)]  # Replace with the actual closing prices from your dataset
  mse = mean_squared_error(actual_prices, prediction)
  # rmse = np.sqrt(mse)
  print("Root Mean Squared Error (RMSE):", mse)

# Create a new DataFrame to store the forecasted values
  forecast_df = pd.DataFrame({'Closing Price Prediction': prediction}, index=forecast_index)

  print("The Predicted Closing Price After 2 years is: ")
  print(forecast_df.index[-1])
  return forecast_df.index[-1]


# def create(prediction):
#     with conn.cursor() as cursor:
#         cursor.execute('INSERT INTO PREDICTIONS (STOCK, PRED_PRICE) VALUES($s, $s)', prediction['stock'], prediction['pred_price'])
#     conn.commit()
#     conn.close()


app = Flask(__name__)

@app.route('/api/v1/stock/download/<stock>', method=['POST'])
def download_predict(stock):
   df = get_historical_data(symbol=stock)
   print(f"Downloading Complete for the ${stock} data for 3 years")

   return redirect('/api/v1/stock/predict/<stock>', method=['GET'])

@app.route('/api/v1/stock/precdict/<stock>', method=["GET"])
def predict(stock):
   df = pd.read_csv(f"data/{stock}.csv")

   print("--------------------------------------------------")
   print("Entering the Pre-processing of Data")

   df = preprocess_data(df)

   print("-----------------------------------------")

   print("Entering the Model Training Phase")
   pred_price = compute_model(df)

   print("The Modified Data is: ", df)

   print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
   print("Saving the Predicted Price in the Database")

   prediction = pd.DataFrame({'stock_name': [stock], 'prediction': [pred_price]})
  #  create(prediction=prediction)





@app.route('/api/v1/create/stock', method= [POST])
def post():
   if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

   create(request.get_json())
   return 'Song Added'

if __name__ == '__main__':
    app.run()