import time
import pandas as pd
import joblib
import alpaca_trade_api as tradeapi

from config import *
from feature_engine import add_features
from trade_scoring import rank_trades
from risk_manager import position_size


# ======================================
# Alpaca API Connection
# ======================================

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)


# ======================================
# Fetch Market Data
# ======================================

def fetch_data(symbol):

    try:

        if "/" in symbol:

            bars = api.get_crypto_bars(
                symbol,
                INTRADAY_TIMEFRAME,
                limit=LOOKBACK_INTRADAY
            ).df

        else:

            bars = api.get_bars(
                symbol,
                INTRADAY_TIMEFRAME,
                limit=LOOKBACK_INTRADAY
            ).df

        if bars is None or len(bars) == 0:
            return None

        df = bars[["open", "high", "low", "close", "volume"]].copy()

        df["symbol"] = symbol

        return df

    except Exception as e:

        print("Data fetch error:", symbol, e)

        return None


# ======================================
# Generate Trade Signal
# ======================================

def generate_trade(symbol, model):

    df = fetch_data(symbol)

    if df is None:
        return None

    df = add_features(df)

    if len(df) < 50:
        return None

    features = df.drop(columns=["symbol"], errors="ignore")

    try:

        prob = model.predict_proba(features.tail(1))[0][1]

    except:

        return None

    # Probability filter

    if prob < BUY_THRESHOLD:
        return None

    price = df.close.iloc[-1]

    atr = df.atr.iloc[-1]

    tp = price + atr * TP_MULTIPLIER
    sl = price - atr * SL_MULTIPLIER

    profit_pct = ((tp - price) / price) * 100

    size = position_size(ACCOUNT_SIZE, price, sl)

    trade = {

        "symbol": symbol,
        "confidence": round(prob, 3),
        "entry": round(price, 4),
        "tp": round(tp, 4),
        "sl": round(sl, 4),
        "expected_profit_pct": round(profit_pct, 2),
        "position_size": size

    }

    return trade


# ======================================
# Market Scanner
# ======================================

def scan_market(model):

    trades = []

    for symbol in TRADING_SYMBOLS:

        try:

            trade = generate_trade(symbol, model)

            if trade is not None:

                trades.append(trade)

        except Exception as e:

            print("Scan error:", symbol, e)

    if len(trades) == 0:
        return []

    trades = rank_trades(trades)

    return trades[:5]


# ======================================
# Print Trades
# ======================================

def print_trades(trades):

    if len(trades) == 0:

        print("No trades found")

        return

    print("\nTop Trade Opportunities\n")

    for t in trades:

        print(
            t["symbol"],
            "| Confidence:", t["confidence"],
            "| Entry:", t["entry"],
            "| TP:", t["tp"],
            "| SL:", t["sl"],
            "| Profit%:", t["expected_profit_pct"]
        )


# ======================================
# Main Engine Loop
# ======================================

def main():

    print("\n===================================")
    print("AI TRADING ENGINE STARTED")
    print("===================================\n")

    print("Loading model...\n")

    model = joblib.load(INTRADAY_MODEL)

    print("Model loaded\n")

    while True:

        print("\nScanning market...\n")

        trades = scan_market(model)

        print_trades(trades)

        print("\nNext scan in", SCAN_INTERVAL, "seconds\n")

        time.sleep(SCAN_INTERVAL)


# ======================================
# Start Program
# ======================================

if __name__ == "__main__":

    main()