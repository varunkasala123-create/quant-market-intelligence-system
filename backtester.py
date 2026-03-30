import numpy as np
import pandas as pd


def backtest(df, model):

    df = df.copy()

    features = df.drop(columns=["symbol"], errors="ignore")

    probs = model.predict_proba(features)[:,1]

    df["prob"] = probs

    trades = df[df["prob"] > 0.6]

    if len(trades) == 0:
        print("No trades")
        return

    win_rate = (trades["prob"] > 0.5).mean()

    print("Trades:", len(trades))
    print("Win rate:", round(win_rate*100,2))