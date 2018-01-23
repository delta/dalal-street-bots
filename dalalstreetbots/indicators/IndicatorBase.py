"""IndicatorBase class"""

class IndicatorBase(object):
    """IndicatorBase class defines the base class for all indicators"""

    default_settings = {
        "type": "prices" # "prices" or "news". If news, it won't get prices updates
    }

    async def _hidden_init_(self, id, settings, manager):
        self.id = id
        self.settings = settings # TODO: need to use the defaults
        self.__manager = manager

    def update(self, update):
        print("My update got called!", update)
        pass
