"""dumbbot class"""

from bots.BotBase import BotBase

class DumbBot(BotBase):
    """DumbBot class defines a dumb bot"""

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
    }

    async def load_indicators(self):
        self.dumb_indicator = await self.get_indicator("DumbIndicator", 1, {})

    def update(self, *args, **kwargs):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""
        print("DumbBot(" + self.name + ") update got called with ", args, kwargs)
