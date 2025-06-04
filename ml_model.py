import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

MODEL_PATH = "forex_model.pkl"

def prepare_features(df):
    features = df[['rsi', 'macd', 'ema_21', 'ema_50', 'bb_high', 'bb_low']].copy()
    from price_action import is_bullish_engulfing, is_bearish_engulfing, is_pin_bar
    features['bullish_engulfing'] = [int(is_bullish_engulfing(df.iloc[:i+1])) for i in range(len(df))]
    features['bearish_engulfing'] = [int(is_bearish_engulfing(df.iloc[:i+1])) for i in range(len(df))]
    features['pin_bar'] = [int(is_pin_bar(df.iloc[:i+1])) for i in range(len(df))]
    return features.fillna(0)

def train_model(df):
    features = prepare_features(df)
    target = (df['close'].shift(-1) > df['close']).astype(int)[:-1]
    features = features[:-1]
    model = RandomForestClassifier(n_estimators=100)
    model.fit(features, target)
    joblib.dump(model, MODEL_PATH)
    return model

def predict_next(df):
    if not os.path.exists(MODEL_PATH):
        train_model(df)
    model = joblib.load(MODEL_PATH)
    features = prepare_features(df)
    probs = model.predict_proba(features.tail(1))[0]
    prediction = "UP" if probs[1] > 0.5 else "DOWN"
    confidence = round(100 * max(probs), 2)
    return prediction, confidence
