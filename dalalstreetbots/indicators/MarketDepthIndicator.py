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
        self.is_first = True
        self.max_buy = 0
        self.min_sell = 0

    def update(self, update):
        if self.is_first:
            self.ask_depth = update.ask_depth
            self.bid_depth = update.bid_depth
        else:
            for price in update.ask_depth_diff:
                if price not in self.ask_depth:
                    self.ask_depth[price] = 0
                self.ask_depth[price] += update.ask_depth_diff[price]
                if self.ask_depth[price] < 0:
                    del self.ask_depth[price]

                if self.min_sell > self.ask_depth[price]:
                    self.min_sell = self.ask_depth[price]

            for price in update.bid_depth_diff:
                if price not in self.bid_depth:
                    self.bid_depth[price] = 0
                self.bid_depth[price] += update.bid_depth_diff[price]
                if self.bid_depth[price] < 0:
                    del self.bid_depth[price]

                if self.max_buy < self.bid_depth[price]:
                    self.max_buy = self.bid_depth[price]

        self.is_first = False