import pandas as pd
import numpy as np
import joblib

from lightgbm import LGBMClassifier
from feature_engine import add_features


def train_model(df, horizon=5, model_name="models/model.pkl"):

    df = df.sort_index()

    print("Total dataset rows:", len(df))

    df = add_features(df)

    # ===============================
    # ATR NORMALIZED TARGET
    # ===============================

    future_price = df["close"].shift(-horizon)

    future_return = (future_price - df["close"]) / df["close"]

    atr = (df["high"] - df["low"]).rolling(14).mean()

    atr_pct = atr / df["close"]

    threshold = atr_pct * 0.5

    df["target"] = np.where(
        future_return > threshold, 1,
        np.where(future_return < -threshold, 0, np.nan)
    )

    df = df.replace([np.inf, -np.inf], np.nan)

    df = df.dropna()

    feature_cols = df.columns.tolist()

    for col in ["target", "symbol", "timestamp"]:
        if col in feature_cols:
            feature_cols.remove(col)

    X = df[feature_cols]
    y = df["target"]

    split = int(len(df) * 0.8)

    X_train = X.iloc[:split]
    X_test = X.iloc[split:]

    y_train = y.iloc[:split]
    y_test = y.iloc[split:]

    print("Training rows:", len(X_train))
    print("Validation rows:", len(X_test))
    print("Features used:", len(feature_cols))

    model = LGBMClassifier(
        n_estimators=700,
        learning_rate=0.03,
        max_depth=6,
        num_leaves=32,
        subsample=0.8,
        colsample_bytree=0.8
    )

    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    print("Model accuracy:", accuracy)

    joblib.dump(model, model_name)

    print("Model saved:", model_name)

    return model