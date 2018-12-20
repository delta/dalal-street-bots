from bots.BotBase import BotBase
from math import floor,ceil
class StockBuyerBot(BotBase):
    """This bot closes the gap between the market depth"""

    default_settings = {
        "sleep_duration": 3, # in seconds. THIS SETTING IS REQUIRED
        "buy_limit": 3, # number of companies to buy at a time
        "stocks_per_company":3, # how many stocks per company do you want to buy at a time
        "holding_time": 5, # how many rounds to hold before you sell your stocks off
        "no_of_companies": 12, # number of companies to buy from
        "bot_tag": "unset", # special tags for searching purpose
    }

    def __init__(self):
        self.settings = {}
        self.settings = {**self.default_settings, **self.settings}
        self.current_time = 0 # how many instances have occured since last buying 
        self.company_list = [] # array of [company_id, ema , latest_price]

    async def load_indicators(self):
        self.depthindicator = {}
        self.stockchanger = {}

        for i in range(1, self.settings["no_of_companies"]+1):
            self.depthindicator[i] = await self.get_indicator("MarketDepthIndicator", i, {
                "update_type": "market_depth",
            })
        
        for i in range(1, self.settings["no_of_companies"]+1):
            self.stockchanger[i] = await self.get_indicator("StockchangerIndicator", i, {
                "type": "prices",
            })

    async def update(self, *args, **kwargs):
        try:
            for i in range(1, self.settings['no_of_companies'] + 1):
                min_sell = self.depthindicator[i].min_sell
                max_buy    = self.depthindicator[i].max_buy
                difference = min_sell - max_buy

                if min_sell == 1e9:
                    buy_price = ceil(0.97*max_buy)
                elif difference >= 10:
                    buy_price = ceil(difference*0.1 + max_buy)

                await self.place_buy_order(i, self.settings['stocks_per_company'], buy_price, 0)
                log_message = "StockBuyerBot({}) placed a buy order for company {} at price {}".format(self.name, str(i), str(buy_price))
                print(log_message)
                self.add_to_log(self.id, log_message)
        except Exception as e:
            log_message = "StockBuyer({}) just broke. Cause: {}".format(self.name, str(e))
            print(log_message)
            self.add_to_log(self.id, log_message)