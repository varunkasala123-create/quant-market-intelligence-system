def detect_market_regime(df):

    ema50=df.ema50.iloc[-1]
    ema200=df.ema200.iloc[-1]

    atr=df.atr.iloc[-1]
    price=df.close.iloc[-1]

    vol=atr/price

    if ema50>ema200 and vol>0.001:
        return "UPTREND"

    elif ema50<ema200 and vol>0.001:
        return "DOWNTREND"

    else:
        return "SIDEWAYS"