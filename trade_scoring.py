import pandas as pd


def score_trade(trade):

    score = 0

    score += trade["confidence"] * 50
    score += trade["expected_profit_pct"] * 5

    if trade["signal"] == "BUY":
        score += 5

    return score


def rank_trades(trades):

    if len(trades) == 0:
        return []

    df = pd.DataFrame(trades)

    df["score"] = df.apply(score_trade, axis=1)

    df = df.sort_values("score", ascending=False)

    return df.to_dict("records")