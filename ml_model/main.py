#**************** IMPORT PACKAGES ********************
from flask import Flask, render_template, request, flash, redirect, url_for
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import math, random
from datetime import datetime
import datetime as dt
import yfinance as yf
import tweepy
import preprocessor as p
import re
from sklearn.linear_model import LinearRegression
from textblob import TextBlob
import constants as ct
from Tweet import Tweet

# Ignore Warnings
import warnings
warnings.filterwarnings("ignore")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#***************** FLASK *****************************
app = Flask(__name__)

#To control caching so as to save and retrieve plot figs on client side
@app.after_request
def add_header(response):
    response.headers['Pragma'] = 'no-cache'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/predict',methods = ['POST'])
def insertintotable():
    nm = request.form['nm']

    #**************** FUNCTIONS TO FETCH DATA ***************************
    def get_historical(quote):
        end = datetime.now()
        start = datetime(end.year-2,end.month,end.day)
        data = yf.download(quote, start=start, end=end)
        df = pd.DataFrame(data=data)
        df.to_csv(''+quote+'.csv')

        # If the Data is empty, then we use Alpha_Vantage
        if(df.empty):
            ts = TimeSeries(key='N6A6QT6IBFJOPJ70',output_format='pandas')
            data, meta_data = ts.get_daily_adjusted(symbol='NSE:'+quote, outputsize='full')
            #Format df
            #Last 2 yrs rows => 502, in ascending order => ::-1
            data=data.head(503).iloc[::-1]
            data=data.reset_index()
            #Keep Required cols only
            df=pd.DataFrame()
            df['Date']=data['date']
            df['Open']=data['1. open']
            df['High']=data['2. high']
            df['Low']=data['3. low']
            df['Close']=data['4. close']
            df['Adj Close']=data['5. adjusted close']
            df['Volume']=data['6. volume']
            df.to_csv(''+quote+'.csv',index=False)
        return

    #******************** ARIMA SECTION ********************
    def ARIMA_ALGO(df):
        uniqueVals = df["Code"].unique()  
        len(uniqueVals)
        df=df.set_index("Code")
        #for daily basis
        def parser(x):
            return datetime.strptime(x, '%Y-%m-%d')
        def arima_model(train, test):
            history = [x for x in train]
            predictions = list()
            for t in range(len(test)):
                model = ARIMA(history, order=(6,1 ,0))
                model_fit = model.fit(disp=0)
                output = model_fit.forecast()
                yhat = output[0]
                predictions.append(yhat[0])
                obs = test[t]
                history.append(obs)
            return predictions
        for company in uniqueVals[:10]:
            data=(df.loc[company,:]).reset_index()
            data['Price'] = data['Close']
            Quantity_date = data[['Price','Date']]
            Quantity_date.index = Quantity_date['Date'].map(lambda x: parser(x))
            Quantity_date['Price'] = Quantity_date['Price'].map(lambda x: float(x))
            Quantity_date = Quantity_date.fillna(Quantity_date.bfill())
            Quantity_date = Quantity_date.drop(['Date'],axis =1)
            fig = plt.figure(figsize=(7.2,4.8),dpi=65)
            plt.plot(Quantity_date)
            plt.savefig('static/Trends.png')
            plt.close(fig)
            
            quantity = Quantity_date.values
            size = int(len(quantity) * 0.80)
            train, test = quantity[0:size], quantity[size:len(quantity)]
            #fit in model
            predictions = arima_model(train, test)
            
            #plot graph
            fig = plt.figure(figsize=(7.2,4.8),dpi=65)
            plt.plot(test,label='Actual Price')
            plt.plot(predictions,label='Predicted Price')
            plt.legend(loc=4)
            plt.savefig('static/ARIMA.png')
            plt.close(fig)
            print()
            print("##############################################################################")
            arima_pred=predictions[-2]
            print("Tomorrow's",quote," Closing Price Prediction by ARIMA:",arima_pred)
            #rmse calculation
            error_arima = math.sqrt(mean_squared_error(test, predictions))
            print("ARIMA RMSE:",error_arima)
            print("##############################################################################")
            return arima_pred, error_arima
        
# Recommending the Stock based upon the History

    def recommending(df, global_polarity,today_stock,mean):
        if today_stock.iloc[-1]['Close'] < mean:
            if global_polarity > 0:
                idea="RISE"
                decision="BUY"
                print()
                print("##############################################################################")
                print("According to the ML Predictions and Sentiment Analysis of Tweets, a",idea,"in",quote,"stock is expected => ",decision)
            elif global_polarity <= 0:
                idea="FALL"
                decision="SELL"
                print()
                print("##############################################################################")
                print("According to the ML Predictions and Sentiment Analysis of Tweets, a",idea,"in",quote,"stock is expected => ",decision)
        else:
            idea="FALL"
            decision="SELL"
            print()
            print("##############################################################################")
            print("According to the ML Predictions and Sentiment Analysis of Tweets, a",idea,"in",quote,"stock is expected => ",decision)
        return idea, decision

        
    quote=nm
    #Try-except to check if valid stock symbol
    try:
        get_historical(quote)
    except:
        return render_template('index.html',not_found=True)
    else:
        df = pd.read_csv(''+quote+'.csv')
        print("##############################################################################")
        print("Today's",quote,"Stock Data: ")
        today_stock=df.iloc[-1:]
        print(today_stock)
        print("##############################################################################")
        df = df.dropna()
        code_list=[]
        for i in range(0,len(df)):
            code_list.append(quote)
        df2=pd.DataFrame(code_list,columns=['Code'])
        df2 = pd.concat([df2, df], axis=1)
        df=df2


        arima_pred, error_arima=ARIMA_ALGO(df)
        lstm_pred, error_lstm=LSTM_ALGO(df)
        df, lr_pred, forecast_set,mean,error_lr=LIN_REG_ALGO(df)
        polarity,tw_list,tw_pol,pos,neg,neutral = retrieving_tweets_polarity(quote)
        
        idea, decision=recommending(df, polarity,today_stock,mean)
        print()
        print("Forecasted Prices for Next 7 days:")
        print(forecast_set)
        today_stock=today_stock.round(2)
        return render_template('results.html',quote=quote,arima_pred=round(arima_pred,2),lstm_pred=round(lstm_pred,2),
                               lr_pred=round(lr_pred,2),open_s=today_stock['Open'].to_string(index=False),
                               close_s=today_stock['Close'].to_string(index=False),adj_close=today_stock['Adj Close'].to_string(index=False),
                               tw_list=tw_list,tw_pol=tw_pol,idea=idea,decision=decision,high_s=today_stock['High'].to_string(index=False),
                               low_s=today_stock['Low'].to_string(index=False),vol=today_stock['Volume'].to_string(index=False),
                               forecast_set=forecast_set,error_lr=round(error_lr,2),error_lstm=round(error_lstm,2),error_arima=round(error_arima,2))
if __name__ == '__main__':
   app.run()