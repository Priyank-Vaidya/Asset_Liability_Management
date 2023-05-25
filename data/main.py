import yfinance as yf
import pandas as pd
from datetime import datetime

def get_historical_data(symbol):
    end = datetime.now()
    start = datetime(end.year - 3, end.month, end.day)
    data = yf.download(symbol, start=start, end=end)
    df = pd.DataFrame(data=data)
    df.to_csv(f'{symbol}.csv', index=False)
    print("Downloading CSV")
    return df

get_historical_data('GOOGL')