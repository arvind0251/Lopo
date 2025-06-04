import ta

def add_indicators(df):
    df['rsi'] = ta.momentum.rsi(df['close'], window=14, fillna=True)
    df['macd'] = ta.trend.macd_diff(df['close'], fillna=True)
    df['ema_21'] = ta.trend.ema_indicator(df['close'], window=21, fillna=True)
    df['ema_50'] = ta.trend.ema_indicator(df['close'], window=50, fillna=True)
    df['bb_high'] = ta.volatility.bollinger_hband(df['close'], window=20, fillna=True)
    df['bb_low'] = ta.volatility.bollinger_lband(df['close'], window=20, fillna=True)
    return df
