"""dumbbot class"""

from bots.BotBase import BotBase

class DumbBot(BotBase):
    """DumbBot class defines a dumb bot"""

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
    }

    def __init__(self):
        self.__bought = False

    async def load_indicators(self):
        self.dumb_indicator = await self.get_indicator("DumbIndicator", 1, {})

    async def update(self, *args, **kwargs):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""
        my_cash = await self.get_my_cash()

        if not self.__bought and self.name == "testbot2":
            await self.buy_stocks_from_exchange(1, 5)
            self.__bought = True
