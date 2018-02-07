from bots.BotBase import BotBase
import random
import decimal

class StockSellerBot(BotBase):
    """Bot that changes prices randomly"""

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
    }

    def __init__(self):
        self.__bought = False

    async def load_indicators(self):
        self.priceindicator = {}
        for i in range(1,10):
            self.priceindicator[i] = await self.get_indicator("PricechangerIndicator", i, {})

    async def update(self, *args, **kwargs):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""
        print("StockBuyerBot(" + self.name + ") was called")

        if not self.__bought:
            random_stock = 1
            stock_price  = self.priceindicator[random_stock].price
            if stock_price != 0:
                random_const = float(decimal.Decimal(random.randrange(-5,5))/100)
                stock_price = (1+random_const)*stock_price
                stock_price = int(stock_price)
                await self.place_sell_order(random_stock, 1, stock_price)
                log_message = "StockBuyerBot(" + self.name + ") bought ", str(random_stock)
            else:
                log_message = "StockBuyerBot(" + self.name + ") bought nothing"
            self.add_to_log(self.id, log_message)