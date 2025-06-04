def is_bullish_engulfing(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    return (last['close'] > last['open'] and prev['close'] < prev['open'] and
            last['close'] > prev['open'] and last['open'] < prev['close'])

def is_bearish_engulfing(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    return (last['close'] < last['open'] and prev['close'] > prev['open'] and
            last['open'] > prev['close'] and last['close'] < prev['open'])

def is_pin_bar(df):
    last = df.iloc[-1]
    body = abs(last['close'] - last['open'])
    candle_length = last['high'] - last['low']
    upper_shadow = last['high'] - max(last['close'], last['open'])
    lower_shadow = min(last['close'], last['open']) - last['low']
    return (body < candle_length * 0.3) and (upper_shadow > body * 2 or lower_shadow > body * 2)
