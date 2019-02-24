from bots.BotBase import BotBase
import random
import traceback

class MarketmakerBot(BotBase):
    """Marketmaker bot acts as the market maker for Dalalstreet

    Look for companies which have a large spread. More the spread, more the profit
    for the market maker. Place buy @ max(buyDepth) + e and Place sell at
    @ min(sellDepth) - e. This puts the market maker ahead in the order depth and tries to
    give him the spread profit.
    """

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
        "no_of_companies": 15, # number of companies to buy from. Technically should be ALL
        "bot_tag": "unset", # special tags for searching purpose
        "e_start": 2, # value of e will go from [e_start, e_end]
        "e_end": 4, # value of e will go from [e_start, e_end]
        "percent_diff": 2 # if bid spread percent is less than this, do nothing
    }

    def __init__(self):
        self.settings = {}
        self.settings = {**self.default_settings, **self.settings}
        self.current_time = 0 # how many instances have occured since last buying
        self.last_buy_price = 0 # if the last_buy_price is max_buy, then you already have the highest bid
        self.last_sell_price = 10**9 # if the last_sell_price is min_sell, then you already have the lowest ask

    async def load_indicators(self):
        self.marketdepthindicator = {}
        self.stockchangerindicator = {}

        for i in range(1, self.settings["no_of_companies"]+1):
            self.marketdepthindicator[i] = await self.get_indicator("MarketmakerIndicator", i, {})
        for i in range(1, self.settings["no_of_companies"]+1):
            self.stockchangerindicator[i] = await self.get_indicator("StockchangerIndicator", i, {})

    async def update(self, *args, **kwargs):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""
        try:
            selected_stock = 0
            max_percent_diff = 0
            e = random.randint(self.settings['e_start'], self.settings['e_end'])
            for stock_id in range(1, self.settings['no_of_companies']+1):
                if self.marketdepthindicator[stock_id].first_update_done and self.stockchangerindicator[stock_id].price > 0:
                    max_buy = self.marketdepthindicator[stock_id].max_buy
                    min_sell = self.marketdepthindicator[stock_id].min_sell
                    max_buy_is_market_order = self.marketdepthindicator[stock_id].max_buy_is_market_order
                    min_sell_is_market_order = self.marketdepthindicator[stock_id].min_sell_is_market_order
                    current_price = self.stockchangerindicator[stock_id].price
                    if max_buy_is_market_order or max_buy == 0:
                        max_buy = int(round(current_price*0.85))
                    if min_sell_is_market_order or min_sell == 10**9:
                        min_sell = int(round(current_price*1.15))

                    percent_diff = (min_sell - max_buy)/max_buy*100
                    if percent_diff > max_percent_diff:
                        selected_stock = stock_id
                        max_percent_diff = percent_diff
            if max_percent_diff > self.settings['percent_diff']:
                qty1 = random.randint(1,3)
                qty2 = random.randint(1,3)
                if max_buy >= self.last_buy_price:
                    await self.place_buy_order(selected_stock, int(qty1), int(max_buy + e), 0)
                    self.last_buy_price = int(max_buy + e)
                if min_sell <= self.last_sell_price:
                    await self.place_sell_order(selected_stock, int(qty2), int(min_sell - e), 0)
                    self.last_sell_price = int(min_sell - e)

        except Exception as e:
            log_message = "MarketmakerBot({}) just broke. Cause: {}".format(self.name, str(e))
            print(log_message)
            error_traceback = ''.join(traceback.format_tb(e.__traceback__))
            error_message = "Got Error: {} @@@ {}".format(str(e), error_traceback)
            self.write_to_logs(self.id, error_message)
