# =============================
# API SETTINGS
# =============================

API_KEY = "api key paste here"
SECRET_KEY = "secret key paste here"
BASE_URL = "https://paper-api.alpaca.markets"


# =============================
# TIMEFRAME SETTINGS
# =============================

INTRADAY_TIMEFRAME = "5Min"
SWING_TIMEFRAME = "30Min"

LOOKBACK_INTRADAY = 8000
LOOKBACK_SWING = 12000

SCAN_INTERVAL = 300


# =============================
# TRADING UNIVERSE
# =============================

TRADING_SYMBOLS = [

# Crypto
"BTC/USD","ETH/USD","SOL/USD","AVAX/USD","LINK/USD",
"ADA/USD","DOT/USD","LTC/USD",

# Stocks
"NVDA","AAPL","MSFT","TSLA","AMZN","META","AMD","NFLX",

# ETFs
"SPY","QQQ","IWM","DIA","XLF","XLK","XLE"

]


# =============================
# RISK SETTINGS
# =============================

ACCOUNT_SIZE = 10000

RISK_PER_TRADE = 0.01

TP_MULTIPLIER = 1.5
SL_MULTIPLIER = 0.7


# =============================
# MODEL SETTINGS
# =============================

INTRADAY_MODEL = "models/intraday_model.pkl"
SWING_MODEL = "models/swing_model.pkl"

BUY_THRESHOLD = 0.60
SELL_THRESHOLD = 0.40