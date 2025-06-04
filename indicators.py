import ta

def add_indicators(df):
    """
    DataFrame me trading indicators add karta hai:
    - RSI
    - MACD diff
    - EMA 21, EMA 50
    - SMA 20, SMA 50
    - Bollinger Bands (High/Low)
    - ATR (Average True Range)
    - Stochastic Oscillator (k%, d%)
    - CCI (Commodity Channel Index)
    - ADX (Average Directional Index)
    - Williams %R
    NaN values ko fill karta hai (fillna=True).
    Args:
        df: pandas DataFrame with at least a 'close' price column.
    Returns:
        df: DataFrame with new indicator columns.
    """
    # Make sure 'close' column is float
    df['close'] = df['close'].astype(float)

    # RSI
    df['rsi'] = ta.momentum.rsi(df['close'], window=14, fillna=True)
    # MACD diff (MACD line - Signal line)
    df['macd'] = ta.trend.macd_diff(df['close'], fillna=True)
    # EMA 21, EMA 50
    df['ema_21'] = ta.trend.ema_indicator(df['close'], window=21, fillna=True)
    df['ema_50'] = ta.trend.ema_indicator(df['close'], window=50, fillna=True)
    # SMA 20, SMA 50
    df['sma_20'] = ta.trend.sma_indicator(df['close'], window=20, fillna=True)
    df['sma_50'] = ta.trend.sma_indicator(df['close'], window=50, fillna=True)
    # Bollinger Bands
    df['bb_high'] = ta.volatility.bollinger_hband(df['close'], window=20, fillna=True)
    df['bb_low'] = ta.volatility.bollinger_lband(df['close'], window=20, fillna=True)
    # ATR
    df['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14, fillna=True)
    # Stochastic Oscillator
    df['stoch_k'] = ta.momentum.stoch(df['high'], df['low'], df['close'], window=14, smooth_window=3, fillna=True)
    df['stoch_d'] = ta.momentum.stoch_signal(df['high'], df['low'], df['close'], window=14, smooth_window=3, fillna=True)
    # CCI
    df['cci'] = ta.trend.cci(df['high'], df['low'], df['close'], window=20, fillna=True)
    # ADX
    df['adx'] = ta.trend.adx(df['high'], df['low'], df['close'], window=14, fillna=True)
    # Williams %R
    df['williams_r'] = ta.momentum.williams_r(df['high'], df['low'], df['close'], lbp=14, fillna=True)

    return df
