import pandas as pd
import requests
from config import API_KEY  # Make sure your Alpha Vantage API key is in config.py

def fetch_candles(symbol="USDJPY", interval="1min", count=100):
    # Alpha Vantage FX_INTRADAY API: https://www.alphavantage.co/documentation/#fx-intraday
    # symbol: e.g. "USDJPY"
    from_symbol = symbol[:3]
    to_symbol = symbol[3:]
    url = (
        f"https://www.alphavantage.co/query?function=FX_INTRADAY"
        f"&from_symbol={from_symbol}&to_symbol={to_symbol}"
        f"&interval={interval}&outputsize=compact&apikey={API_KEY}"
    )
    r = requests.get(url)
    data = r.json()
    key = f"Time Series FX ({interval})"
    if key not in data:
        raise ValueError(f"Alpha Vantage API error or data unavailable: {data.get('Note') or data.get('Error Message') or data}")
    df = pd.DataFrame.from_dict(data[key], orient='index')
    df = df.rename(columns={
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close'
    })
    # Convert index to datetime and sort
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    # Convert all columns to float
    df = df.astype(float)
    # Only keep last 'count' rows
    df = df.tail(count)
    df = df.reset_index().rename(columns={'index': 'datetime'})
    return df
