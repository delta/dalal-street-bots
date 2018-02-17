from bots.BotBase import BotBase
import random
import decimal

class StockBuyerBot(BotBase):
    """Bot that changes prices randomly"""

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
        "buy_limit": 3, # number of companies to buy at a time
        "stocks_per_company":3, # how many stocks per company do you want to buy at a time
        "holding_time": 5, # how many rounds to hold before you sell your stocks off
        "no_of_companies": 10, # number of companies to buy from
        "bot_tag": "unset", # special tags for searching purpose
    }

    def __init__(self):
        self.settings = {}
        self.settings = {**self.default_settings, **self.settings}
        self.__bought = False

    async def load_indicators(self):
        self.priceindicator = {}
        for i in range(1,10):
            self.priceindicator[i] = await self.get_indicator("PricechangerIndicator", i, {})

    async def update(self, *args, **kwargs):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""
        if not self.__bought:
            random_stock = 1
            stock_price  = self.priceindicator[random_stock].price
            if stock_price != 0:
                random_const = float(decimal.Decimal(random.randrange(-5,5))/100)
                stock_price  = stock_price + stock_price*random_const
                stock_price  = int(stock_price)
                await self.place_buy_order(random_stock, self.settings["stocks_per_company"], stock_price, 1)
                log_message = "StockBuyerBot(" + self.name + ") bought " + str(random_stock)
                print(log_message)
            else:
                log_message = "StockBuyerBot(" + self.name + ") bought nothing"
                print(log_message)
            self.add_to_log(self.id, log_message)
