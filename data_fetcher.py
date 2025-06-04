import pandas as pd
import requests
from config import API_KEY

def fetch_candles(symbol="USDJPY", interval="1min", count=200):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&apikey={API_KEY}&outputsize={count}"
    r = requests.get(url)
    data = r.json()
    print("API RESPONSE:", data)  # Add this line for debugging
    if "values" not in data:
        raise ValueError(f"API error or no data: {data}")
    df = pd.DataFrame(data['values'])
    df = df.iloc[::-1]
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    return df
