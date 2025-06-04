import ta

def add_indicators(df):
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)
    df['macd'] = ta.trend.macd_diff(df['close'])
    df['ema_21'] = ta.trend.ema_indicator(df['close'], window=21)
    df['ema_50'] = ta.trend.ema_indicator(df['close'], window=50)
    df['bb_high'] = ta.volatility.bollinger_hband(df['close'], window=20)
    df['bb_low'] = ta.volatility.bollinger_lband(df['close'], window=20)
    return df
