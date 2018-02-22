from indicators.IndicatorBase import IndicatorBase
from math import ceil
class MarketDepthIndicator(IndicatorBase):

    default_settings = {
        "k": 3  # value of k in k-EMA
    }

    update_type = "market_depth"

    def __init__(self):
        print("inited")
        # private, not required outside
        self.__first_update_done = False
        
        self.ask_depth = {}
        self.bid_depth = {}
        self.max_buy_is_market_order = False
        self.min_sell_is_market_order = False
        self.max_buy = -1
        self.min_sell = 1e9
        self.ismarket = True

    def update(self, first_update, update):
        print("Got market update")
        if not self.__first_update_done:
            self.__first_update_done = True

            for price in update.ask_depth:
                self.ask_depth[price] = update.ask_depth[price]
            
            for price in update.bid_depth:
                self.bid_depth[price] = update.bid_depth[price]
            
        else:
            for price in update.ask_depth_diff:
                if price not in self.ask_depth:
                    self.ask_depth[price] = 0
                self.ask_depth[price] += update.ask_depth_diff[price]
                if self.ask_depth[price] < 0:
                    del self.ask_depth[price]

            for price in update.bid_depth_diff:
                if price not in self.bid_depth:
                    self.bid_depth[price] = 0
                self.bid_depth[price] += update.bid_depth_diff[price]
                if self.bid_depth[price] < 0:
                    del self.bid_depth[price]

        self.min_sell = 1e9
        for price in self.ask_depth:
            self.min_sell = min((self.min_sell, price))
        
        self.max_buy = 0
        for price in self.bid_depth:
            self.max_buy = max((self.max_buy, price))

        self.max_buy_is_market_order = self.max_buy == 0
        self.min_sell_is_market_order = self.min_sell == 0