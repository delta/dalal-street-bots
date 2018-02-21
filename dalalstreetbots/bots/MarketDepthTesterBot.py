"""dumbbot class"""

from bots.BotBase import BotBase

class MarketDepthTesterBot(BotBase):
    """MarketDepthTesterBot class defines a dumb bot"""

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
    }

    def __init__(self):
        self.__bought = False

    async def load_indicators(self):
        self.indicator = await self.get_indicator("MarketDepthIndicator", 1, {})

    async def update(self, *args, **kwargs):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""
        pass
