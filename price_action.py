def is_bullish_engulfing(df):
    if len(df) < 2:
        return False
    last = df.iloc[-1]
    prev = df.iloc[-2]
    return (
        prev['close'] < prev['open'] and
        last['close'] > last['open'] and
        last['open'] < prev['close'] and
        last['close'] > prev['open']
    )

def is_bearish_engulfing(df):
    if len(df) < 2:
        return False
    last = df.iloc[-1]
    prev = df.iloc[-2]
    return (
        prev['close'] > prev['open'] and
        last['close'] < last['open'] and
        last['open'] > prev['close'] and
        last['close'] < prev['open']
    )

def is_pin_bar(df):
    if len(df) < 1:
        return False
    last = df.iloc[-1]
    body = abs(last['close'] - last['open'])
    candle_length = last['high'] - last['low']
    upper_shadow = last['high'] - max(last['close'], last['open'])
    lower_shadow = min(last['close'], last['open']) - last['low']
    return (
        candle_length > 0 and
        body < candle_length * 0.3 and
        (upper_shadow > body * 2 or lower_shadow > body * 2)
    )

def is_doji(df, tol=0.05):
    if len(df) < 1:
        return False
    last = df.iloc[-1]
    return abs(last['close'] - last['open']) <= (last['high'] - last['low']) * tol

def is_hammer(df):
    if len(df) < 1:
        return False
    last = df.iloc[-1]
    body = abs(last['close'] - last['open'])
    lower_shadow = min(last['close'], last['open']) - last['low']
    upper_shadow = last['high'] - max(last['close'], last['open'])
    candle_length = last['high'] - last['low']
    return (
        candle_length > 0 and
        lower_shadow > 2 * body and
        upper_shadow < body
    )

def is_inverted_hammer(df):
    if len(df) < 1:
        return False
    last = df.iloc[-1]
    body = abs(last['close'] - last['open'])
    lower_shadow = min(last['close'], last['open']) - last['low']
    upper_shadow = last['high'] - max(last['close'], last['open'])
    candle_length = last['high'] - last['low']
    return (
        candle_length > 0 and
        upper_shadow > 2 * body and
        lower_shadow < body
    )

def is_shooting_star(df):
    # Like inverted hammer but in uptrend (context not checked here)
    return is_inverted_hammer(df)

def is_morning_star(df):
    if len(df) < 3:
        return False
    c1, c2, c3 = df.iloc[-3], df.iloc[-2], df.iloc[-1]
    return (
        c1['close'] < c1['open'] and
        is_doji(df.iloc[[-2]]) and
        c3['close'] > c3['open'] and
        c3['close'] > ((c1['open'] + c1['close']) / 2)
    )

def is_evening_star(df):
    if len(df) < 3:
        return False
    c1, c2, c3 = df.iloc[-3], df.iloc[-2], df.iloc[-1]
    return (
        c1['close'] > c1['open'] and
        is_doji(df.iloc[[-2]]) and
        c3['close'] < c3['open'] and
        c3['close'] < ((c1['open'] + c1['close']) / 2)
    )

def is_three_white_soldiers(df):
    if len(df) < 3:
        return False
    c1, c2, c3 = df.iloc[-3], df.iloc[-2], df.iloc[-1]
    return (
        c1['close'] > c1['open'] and
        c2['close'] > c2['open'] and
        c3['close'] > c3['open'] and
        c2['open'] > c1['open'] and c2['close'] > c1['close'] and
        c3['open'] > c2['open'] and c3['close'] > c2['close']
    )

def is_three_black_crows(df):
    if len(df) < 3:
        return False
    c1, c2, c3 = df.iloc[-3], df.iloc[-2], df.iloc[-1]
    return (
        c1['close'] < c1['open'] and
        c2['close'] < c2['open'] and
        c3['close'] < c3['open'] and
        c2['open'] < c1['open'] and c2['close'] < c1['close'] and
        c3['open'] < c2['open'] and c3['close'] < c2['close']
    )

def is_marubozu_bullish(df, tol=0.01):
    if len(df) < 1:
        return False
    last = df.iloc[-1]
    body = abs(last['close'] - last['open'])
    candle_length = last['high'] - last['low']
    upper_shadow = last['high'] - max(last['close'], last['open'])
    lower_shadow = min(last['close'], last['open']) - last['low']
    return (
        last['close'] > last['open'] and
        upper_shadow < candle_length * tol and
        lower_shadow < candle_length * tol
    )

def is_marubozu_bearish(df, tol=0.01):
    if len(df) < 1:
        return False
    last = df.iloc[-1]
    body = abs(last['close'] - last['open'])
    candle_length = last['high'] - last['low']
    upper_shadow = last['high'] - max(last['close'], last['open'])
    lower_shadow = min(last['close'], last['open']) - last['low']
    return (
        last['close'] < last['open'] and
        upper_shadow < candle_length * tol and
        lower_shadow < candle_length * tol
    )

def is_spinning_top(df, tol=0.3):
    if len(df) < 1:
        return False
    last = df.iloc[-1]
    body = abs(last['close'] - last['open'])
    candle_length = last['high'] - last['low']
    upper_shadow = last['high'] - max(last['close'], last['open'])
    lower_shadow = min(last['close'], last['open']) - last['low']
    return (
        candle_length > 0 and
        body <= candle_length * tol and
        upper_shadow > body and
        lower_shadow > body
    )   )
