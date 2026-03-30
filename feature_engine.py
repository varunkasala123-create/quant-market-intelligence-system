import pandas as pd
import numpy as np


def add_features(df):

    df = df.copy()

    # ===============================
    # Moving Averages
    # ===============================

    df["ema20"] = df["close"].ewm(span=20, adjust=False).mean()
    df["ema50"] = df["close"].ewm(span=50, adjust=False).mean()
    df["ema200"] = df["close"].ewm(span=200, adjust=False).mean()

    # ===============================
    # RSI
    # ===============================

    delta = df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / (avg_loss + 1e-10)

    df["rsi"] = 100 - (100 / (1 + rs))

    # ===============================
    # Momentum
    # ===============================

    df["momentum"] = df["close"] - df["close"].shift(10)

    # ===============================
    # ATR
    # ===============================

    high_low = df["high"] - df["low"]
    high_close = np.abs(df["high"] - df["close"].shift())
    low_close = np.abs(df["low"] - df["close"].shift())

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)

    df["atr"] = tr.rolling(14).mean()

    # ===============================
    # Bollinger Bands
    # ===============================

    df["bb_mid"] = df["close"].rolling(20).mean()

    std = df["close"].rolling(20).std()

    df["bb_upper"] = df["bb_mid"] + 2 * std
    df["bb_lower"] = df["bb_mid"] - 2 * std

    # ===============================
    # Volume Indicators
    # ===============================

    df["vol_change"] = df["volume"].pct_change()

    df["obv"] = (np.sign(df["close"].diff()) * df["volume"]).fillna(0).cumsum()

    # ===============================
    # VWAP
    # ===============================

    df["vwap"] = (
        df["volume"] * (df["high"] + df["low"] + df["close"]) / 3
    ).cumsum() / df["volume"].cumsum()

    # ===============================
    # Returns
    # ===============================

    df["return_1"] = df["close"].pct_change(1)
    df["return_3"] = df["close"].pct_change(3)
    df["return_5"] = df["close"].pct_change(5)
    df["return_10"] = df["close"].pct_change(10)

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    return df