import alpaca_trade_api as tradeapi
from config import API_KEY, SECRET_KEY, BASE_URL

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)


def is_stock_market_open():

    try:

        clock = api.get_clock()

        return clock.is_open

    except:

        return False