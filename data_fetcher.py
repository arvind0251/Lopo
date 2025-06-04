import pandas as pd
import requests
from config import API_KEY

def fetch_candles(symbol="USDJPY", interval="1min", count=100):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&outputsize={count}&apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    if "values" not in data:
        raise ValueError(f"Twelve Data API error: {data.get('message', data)}")
    df = pd.DataFrame(data["values"])
    df = df.iloc[::-1]
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    return df
