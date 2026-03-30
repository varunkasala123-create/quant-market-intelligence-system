import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="AI Trading Dashboard", layout="wide")

st.title("AI Trading System Dashboard")

# ==========================================
# File Paths
# ==========================================

BEST_TRADES = "logs/best_trades.csv"
TRADE_LOG = "logs/trade_journal.csv"
EXECUTED_LOG = "logs/executed_trades.csv"


# ==========================================
# Load Data
# ==========================================

def load_csv(path):

    if os.path.exists(path):

        return pd.read_csv(path)

    return pd.DataFrame()


best_trades = load_csv(BEST_TRADES)
trade_log = load_csv(TRADE_LOG)
executed = load_csv(EXECUTED_LOG)


# ==========================================
# Helper: Profit %
# ==========================================

def profit_percent(entry,tp):

    try:
        return round((tp-entry)/entry*100,2)
    except:
        return 0


# ==========================================
# TOP TRADES SECTION
# ==========================================

st.header("Top 5 AI Trade Opportunities")

if len(best_trades) == 0:

    st.warning("No trade signals yet. Waiting for engine scan.")

else:

    header = st.columns(9)

    header[0].markdown("**Symbol**")
    header[1].markdown("**Signal**")
    header[2].markdown("**Confidence**")
    header[3].markdown("**Entry**")
    header[4].markdown("**TP**")
    header[5].markdown("**SL**")
    header[6].markdown("**Profit %**")
    header[7].markdown("**Time**")
    header[8].markdown("**Execute**")


    for i,row in best_trades.iterrows():

        profit = profit_percent(row["entry"],row["tp"])

        cols = st.columns(9)

        cols[0].write(row["symbol"])
        cols[1].write(row["signal"])
        cols[2].write(row["confidence"])
        cols[3].write(row["entry"])
        cols[4].write(row["tp"])
        cols[5].write(row["sl"])
        cols[6].write(str(profit)+" %")
        cols[7].write(row["time"])

        if cols[8].button("Execute",key=i):

            executed_trade = {

                "time": datetime.now(),
                "symbol": row["symbol"],
                "signal": row["signal"],
                "entry": row["entry"],
                "tp": row["tp"],
                "sl": row["sl"],
                "confidence": row["confidence"]

            }

            df = pd.DataFrame([executed_trade])

            if os.path.exists(EXECUTED_LOG):

                df.to_csv(EXECUTED_LOG,mode="a",header=False,index=False)

            else:

                df.to_csv(EXECUTED_LOG,index=False)

            st.success(f"Executed {row['symbol']}")



# ==========================================
# REFRESH BUTTON
# ==========================================

st.divider()

if st.button("Refresh Signals"):

    st.rerun()



# ==========================================
# EXECUTED TRADES JOURNAL
# ==========================================

st.header("Executed Trades")

if len(executed)==0:

    st.info("No executed trades yet")

else:

    st.dataframe(executed,use_container_width=True)



# ==========================================
# FULL TRADE LOG SECTION
# ==========================================

st.header("Full AI Trade Log")

if len(trade_log)==0:

    st.info("No logs yet")

else:

    trade_log["Executed"] = trade_log["symbol"].isin(
        executed["symbol"] if len(executed)>0 else []
    )

    st.dataframe(trade_log,use_container_width=True)