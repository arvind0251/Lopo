import pandas as pd
import numpy as np
import requests
from config import API_KEY  # Make sure your Twelve Data API key is set here

def fetch_candles(symbol="USDJPY", interval="1min", count=1000):
    # Twelve Data expects forex symbol as "USD/JPY" format
    if "/" not in symbol and len(symbol) == 6:
        symbol = symbol[:3] + "/" + symbol[3:]

    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={symbol}"
        f"&interval={interval}"
        f"&outputsize={count}"
        f"&apikey={API_KEY}"
    )
    r = requests.get(url)
    data = r.json()
    if "values" not in data:
        print("API raw response:", data)  # Debug info in case of error
        raise ValueError(f"Twelve Data API error: {data.get('message', data)}")

    df = pd.DataFrame(data["values"])
    df = df.iloc[::-1]  # reverse to have oldest first

    # Only convert columns that exist (volume is optional!)
    float_cols = [col for col in ['open', 'high', 'low', 'close', 'volume'] if col in df.columns]
    for col in float_cols:
        df[col] = df[col].astype(float)

    # Convert datetime if present and add time-based features
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['hour'] = df['datetime'].dt.hour
        df['minute'] = df['datetime'].dt.minute
        df['day_of_week'] = df['datetime'].dt.dayofweek

    # Extra features for ML
    df['returns'] = df['close'].pct_change().fillna(0)
    df['log_return'] = np.log(df['close'] / df['close'].shift(1)).fillna(0)
    df['volatility'] = df['returns'].rolling(10).std().fillna(0)

    return df
