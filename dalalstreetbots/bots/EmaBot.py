from bots.BotBase import BotBase

class EmaBot(BotBase):
    """The simplest of all the bots. If you lose to this bot, then you should reconsider a future in the market."""

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
    }

    def __init__(self):
        self.__bought = True

    async def load_indicators(self):
        self.emaindicator = await self.get_indicator("EmaIndicator", 1, {})

    async def update(self, *args, **kwargs):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""
        my_cash = await self.get_my_cash()
        print("EmaBot(" + self.name + ") update got called with ", args, kwargs, self.emaindicator.prices)
        print("EmaBot(" + self.name + ") has " + str(my_cash) + " cash")

        if not self.__bought and self.name == "testbot2":
            await self.buy_stocks_from_exchange(1, 5)
            self.__bought = True