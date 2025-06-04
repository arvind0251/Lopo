import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score

MODEL_PATH = "forex_model.pkl"

# Import all price action pattern functions
from price_action import (
    is_bullish_engulfing, is_bearish_engulfing, is_pin_bar,
    is_doji, is_hammer, is_inverted_hammer, is_shooting_star,
    is_morning_star, is_evening_star, is_three_white_soldiers,
    is_three_black_crows, is_marubozu_bullish, is_marubozu_bearish,
    is_spinning_top,
)

# --- IMPORTANT: This list should match retrain_model.py ---
all_features = [
    'rsi', 'macd', 'ema_21', 'ema_50', 'bb_high', 'bb_low',
    'candle_body', 'candle_range', 'upper_shadow', 'lower_shadow', 'candle_direction',
    'bullish_engulfing', 'bearish_engulfing', 'pin_bar', 'doji', 'hammer', 
    'inverted_hammer', 'shooting_star', 'morning_star', 'evening_star', 
    'three_white_soldiers', 'three_black_crows', 'marubozu_bullish', 
    'marubozu_bearish', 'spinning_top'
]

def prepare_features(df):
    """Prepare an extensive feature set for ML."""
    features = pd.DataFrame()
    # Add technical indicators
    for col in ['rsi', 'macd', 'ema_21', 'ema_50', 'bb_high', 'bb_low']:
        features[col] = df[col]

    # Add candle statistics
    features['candle_body'] = abs(df['close'] - df['open'])
    features['candle_range'] = df['high'] - df['low']
    features['upper_shadow'] = df['high'] - df[['close','open']].max(axis=1)
    features['lower_shadow'] = df[['close','open']].min(axis=1) - df['low']
    features['candle_direction'] = (df['close'] > df['open']).astype(int)
    
    # Add price action patterns
    features['bullish_engulfing'] = [int(is_bullish_engulfing(df.iloc[:i+1])) for i in range(len(df))]
    features['bearish_engulfing'] = [int(is_bearish_engulfing(df.iloc[:i+1])) for i in range(len(df))]
    features['pin_bar'] = [int(is_pin_bar(df.iloc[:i+1])) for i in range(len(df))]
    features['doji'] = [int(is_doji(df.iloc[:i+1])) for i in range(len(df))]
    features['hammer'] = [int(is_hammer(df.iloc[:i+1])) for i in range(len(df))]
    features['inverted_hammer'] = [int(is_inverted_hammer(df.iloc[:i+1])) for i in range(len(df))]
    features['shooting_star'] = [int(is_shooting_star(df.iloc[:i+1])) for i in range(len(df))]
    features['morning_star'] = [int(is_morning_star(df.iloc[:i+1])) for i in range(len(df))]
    features['evening_star'] = [int(is_evening_star(df.iloc[:i+1])) for i in range(len(df))]
    features['three_white_soldiers'] = [int(is_three_white_soldiers(df.iloc[:i+1])) for i in range(len(df))]
    features['three_black_crows'] = [int(is_three_black_crows(df.iloc[:i+1])) for i in range(len(df))]
    features['marubozu_bullish'] = [int(is_marubozu_bullish(df.iloc[:i+1])) for i in range(len(df))]
    features['marubozu_bearish'] = [int(is_marubozu_bearish(df.iloc[:i+1])) for i in range(len(df))]
    features['spinning_top'] = [int(is_spinning_top(df.iloc[:i+1])) for i in range(len(df))]
    
    # Clean NaNs and enforce all_features order
    features = features.fillna(0)
    features = features[all_features]
    return features

def train_model(df, verbose=True):
    """Trains the ML model and saves it."""
    features = prepare_features(df)
    target = (df['close'].shift(-1) > df['close']).astype(int)[:-1]
    features = features[:-1]
    
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, shuffle=False)
    
    model = RandomForestClassifier(n_estimators=300, max_depth=8, random_state=42, class_weight="balanced")
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)
    
    if verbose:
        preds = model.predict(X_test)
        report = classification_report(y_test, preds)
        acc = accuracy_score(y_test, preds)
        print("Test Accuracy:", acc)
        print("Classification report:\n", report)
    
    return model

def predict_next(df):
    """Loads model, prepares features, and predicts next candle direction."""
    if not os.path.exists(MODEL_PATH):
        print("Model not found, training new model...")
        train_model(df, verbose=False)
    model = joblib.load(MODEL_PATH)
    features = prepare_features(df)
    last_feat = features.tail(1)
    probs = model.predict_proba(last_feat)[0]
    prediction = "UP" if probs[1] > 0.5 else "DOWN"
    confidence = round(100 * max(probs), 2)
    print("Features for prediction:\n", last_feat)
    print("Prediction probabilities:", probs)
    return prediction, confidence
