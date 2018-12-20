from bots.BotBase import BotBase
from math import floor,ceil
class StockSellerBot(BotBase):
    """This bot closes the gap between the market depth"""

    default_settings = {
        "sleep_duration": 5, # in seconds. THIS SETTING IS REQUIRED
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
        for i in range(1, 2): #self.settings['no_of_companies'] + 1):
            depth = self.depthindicator[i]
            current_price = self.stockchanger[i].price
            
            if current_price == 0:
                # TODO: fix manager to not have to do this shit
                print("bro make a transaction bro")
                return

            """
            Cases:
                Buy has markets -> clear them
                Sell has markets -> do nothing
                sell is empty -> current_price + 15% of current_price.
                buy is empty -> do nothing
                gap between max_buy and min_sell >= 10: order at min(current_price+15%, min_sell - (min_sell-max_buy)/10))
            """

            print("wake up time! ", i, depth.max_buy, depth.min_sell, current_price)

            try:
                if depth.max_buy_is_market_order:
                    await self.place_sell_order(i, self.settings['stocks_per_company'], 0, 1)
                    log_message = "StockSeller({}) placed sell order for company {}".format(self.name, i)
                    print(log_message)
                    self.add_to_log(self.id, log_message)       
                
                elif depth.min_sell == 1e9:
                    sell_price = floor(1.15*current_price)
                    await self.place_sell_order(i, self.settings['stocks_per_company'], sell_price, 0)
                    log_message = "StockSeller({}) placed sell order for company {} at price {}".format(
                        self.name,
                        i,
                        sell_price
                    )
                    print(log_message)
                    self.add_to_log(self.id, log_message)

                elif depth.min_sell - depth.max_buy >= 10:
                    sell_price = min((1.15*current_price, depth.min_sell - (depth.min_sell - depth.max_buy)/15))
                    sell_price = floor(sell_price)
                    await self.place_sell_order(i, self.settings['stocks_per_company'], sell_price, 0)
                    log_message = "StockSeller({}) placed sell order for company {} at price {}".format(
                        self.name,
                        i,
                        sell_price
                    )
                    print(log_message)
                    self.add_to_log(self.id, log_message)
            except Exception as e:
            log_message = "StockSeller({}) just broke. Cause: {}".format(self.name, str(e))
            print(log_message)
            self.add_to_log(self.id, log_message)
