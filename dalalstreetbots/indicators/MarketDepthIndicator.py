from indicators.IndicatorBase import IndicatorBase
from math import ceil
class MarketDepthIndictor(IndicatorBase):

    default_settings = {
        "update_type": "market_depth", # "prices" or "news". If news, it won't get prices updates
        "k": 3  # value of k in k-EMA
    }

    def __init__(self):
        self.ask_depth = {}
        self.bid_depth = {}

    def update(self, update):
        print(update)