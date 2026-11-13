import os
import time
from datetime import datetime
import pandas as pd
import yfinance as yf
import requests

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

TICKER = "AAPL"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d")

def fetch_yahoo_finance_data(ticker=TICKER):
    print(f"Fetching historical data for {ticker} from Yahoo Finance...")
    try:
        df = yf.download(ticker, period="5y", interval="1d", progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        filename = f"{RAW_DIR}/{ticker}_yahoo_historical_{TIMESTAMP}.csv"
        df.to_csv(filename)
        print(f"Successfully saved Yahoo Finance data to {filename}")
        return df
    except Exception as e:
        print(f"Error fetching from Yahoo Finance: {e}")
        return None

def fetch_alpha_vantage_data(ticker=TICKER, api_key="DEMO"):
    print(f"Fetching daily time series for {ticker} from Alpha Vantage...")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if "Time Series (Daily)" in data:
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            filename = f"{RAW_DIR}/{ticker}_alphavantage_daily_{TIMESTAMP}.csv"
            df.to_csv(filename)
            print(f"Successfully saved Alpha Vantage data to {filename}")
            return df
        else:
            print(f"Alpha Vantage message: {data.get('Note', data.get('Error Message', 'Unknown error'))}")
            return None
    except Exception as e:
        print(f"Error connecting to Alpha Vantage: {e}")
        return None

if __name__ == "__main__":
    yf_df = fetch_yahoo_finance_data(TICKER)
    time.sleep(2)
    av_df = fetch_alpha_vantage_data("IBM", api_key="DEMO")
    print("\nData ingestion pipeline complete!")
