from telegram.ext import Updater, CommandHandler
from data_fetcher import fetch_candles
from indicators import add_indicators
from price_action import is_bullish_engulfing, is_bearish_engulfing, is_pin_bar
from ml_model import predict_next
from config import TELEGRAM_TOKEN

def predict(update, context):
    symbol = "USDJPY"  # ya user se input le sakte hain
    df = fetch_candles(symbol)
    df = add_indicators(df)
    pred, conf = predict_next(df)
    patterns = []
    if is_bullish_engulfing(df): patterns.append("Bullish Engulfing")
    if is_bearish_engulfing(df): patterns.append("Bearish Engulfing")
    if is_pin_bar(df): patterns.append("Pin Bar")
    msg = (
        f"Prediction for {symbol} (Next 1-min candle): {pred}\n"
        f"Confidence: {conf}%\n"
        f"Detected patterns: {', '.join(patterns) if patterns else 'None'}"
    )
    update.message.reply_text(msg)

def start(update, context):
    update.message.reply_text("Send /predict to get advanced ML-based candle prediction.")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("predict", predict))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
