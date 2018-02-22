"""dumbbot class"""

from bots.BotBase import BotBase

class MarketDepthTesterBot(BotBase):
    """MarketDepthTesterBot class defines a dumb bot"""

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
    }

    def __init__(self):
        self.settings = {}
        self.settings = {**self.default_settings, **self.settings}
        self.__bought = False

    async def load_indicators(self):
        self.indicator = await self.get_indicator("MarketDepthIndicator", 1, {})

    async def update(self, *args, **kwargs):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""
        print(self.indicator.max_buy, self.indicator.min_sell, self.indicator.max_buy_is_market_order, self.indicator.min_sell_is_market_order)
        print(self.indicator.ask_depth, self.indicator.bid_depth)
        pass
