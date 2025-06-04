import pandas as pd
import requests
from config import TWELVE_DATA_API_KEY

def normalize_symbol(symbol):
    """Accepts EURUSD or EUR/USD, returns EUR/USD."""
    if "/" in symbol:
        return symbol.upper()
    elif len(symbol) == 6:
        return symbol[:3].upper() + "/" + symbol[3:].upper()
    raise ValueError("Invalid symbol, must be 6 chars or contain '/'")

def fetch_candles(symbol="EUR/USD", interval="1min", count=100):
    symbol = normalize_symbol(symbol)
    url = (
        f"https://api.twelvedata.com/time_series?symbol={symbol}"
        f"&interval={interval}&outputsize={count}&apikey={TWELVE_DATA_API_KEY}"
    )
    r = requests.get(url)
    data = r.json()
    if "values" not in data:
        raise ValueError(f"Twelve Data API error: {data.get('message', data)}")
    df = pd.DataFrame(data["values"])
    df = df.iloc[::-1]
    # Convert columns to float
    for col in ['open', 'high', 'low', 'close']:
        df[col] = df[col].astype(float)
    if 'volume' in df.columns:
        df['volume'] = df['volume'].astype(float)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df
