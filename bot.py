from telegram.ext import Updater, CommandHandler
from data_fetcher import fetch_candles
from indicators import add_indicators
from price_action import (
    is_bullish_engulfing, is_bearish_engulfing, is_pin_bar,
    is_doji, is_hammer, is_inverted_hammer, is_shooting_star,
    is_morning_star, is_evening_star, is_three_white_soldiers,
    is_three_black_crows, is_marubozu_bullish, is_marubozu_bearish,
    is_spinning_top
)
from ml_model import predict_next
from config import TELEGRAM_TOKEN

def predict(update, context):
    # User se symbol lo, warna USD/JPY default
    if context.args:
        raw_symbol = context.args[0].replace("/", "").upper()
        symbol = raw_symbol[:3] + "/" + raw_symbol[3:]
    else:
        symbol = "USD/JPY"
    try:
        df = fetch_candles(symbol)
        df = add_indicators(df)
        pred, conf = predict_next(df)
        # All advanced patterns
        patterns = []
        if is_bullish_engulfing(df): patterns.append("Bullish Engulfing")
        if is_bearish_engulfing(df): patterns.append("Bearish Engulfing")
        if is_pin_bar(df): patterns.append("Pin Bar")
        if is_doji(df): patterns.append("Doji")
        if is_hammer(df): patterns.append("Hammer")
        if is_inverted_hammer(df): patterns.append("Inverted Hammer")
        if is_shooting_star(df): patterns.append("Shooting Star")
        if is_morning_star(df): patterns.append("Morning Star")
        if is_evening_star(df): patterns.append("Evening Star")
        if is_three_white_soldiers(df): patterns.append("Three White Soldiers")
        if is_three_black_crows(df): patterns.append("Three Black Crows")
        if is_marubozu_bullish(df): patterns.append("Marubozu Bullish")
        if is_marubozu_bearish(df): patterns.append("Marubozu Bearish")
        if is_spinning_top(df): patterns.append("Spinning Top")
        msg = (
            f"Prediction for {symbol} (Next 1-min candle): {pred}\n"
            f"Confidence: {conf}%\n"
            f"Detected patterns: {', '.join(patterns) if patterns else 'None'}"
        )
    except Exception as e:
        msg = f"Error: {e}"
    update.message.reply_text(msg)

def start(update, context):
    update.message.reply_text(
        "Send /predict SYMBOL (e.g. /predict EURUSD) to get advanced ML-based candle prediction."
    )

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("predict", predict))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
