import pandas as pd
from feature_engine import add_features
from market_regime import detect_market_regime
from risk_manager import position_size
from trade_scoring import trade_score
from config import *

def generate_signal(symbol, df, model):

    df = add_features(df)

    if len(df)<100:
        return None

    features = df.drop(columns=["symbol"],errors="ignore")

    prob = model.predict_proba(features.tail(1))[0][1]

    regime = detect_market_regime(df)

    if regime=="SIDEWAYS":
        return None

    price = df.close.iloc[-1]
    atr = df.atr.iloc[-1]

    tp = price + atr * TP_MULTIPLIER
    sl = price - atr * SL_MULTIPLIER

    reward_risk = (tp-price)/(price-sl)

    score = trade_score(prob,atr,price,reward_risk)

    size = position_size(10000,price,sl)

    return {
        "symbol":symbol,
        "signal":"BUY" if prob>BUY_THRESHOLD else "SELL",
        "confidence":round(prob,3),
        "entry":round(price,2),
        "tp":round(tp,2),
        "sl":round(sl,2),
        "score":round(score,4),
        "position_size":size
    }