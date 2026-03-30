import os
import pandas as pd
import threading

DATASET_PATH="dataset/market_data.parquet"
lock=threading.Lock()

def save_market_data(symbol,df):

    if df is None or len(df)==0:
        return

    df=df.copy()
    df["symbol"]=symbol

    os.makedirs("dataset",exist_ok=True)

    with lock:

        if os.path.exists(DATASET_PATH):

            existing=pd.read_parquet(DATASET_PATH)

            df=pd.concat([existing,df])

            df=df.drop_duplicates()

        df.to_parquet(DATASET_PATH)