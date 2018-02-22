"""IndicatorBase class"""

class IndicatorBase(object):
    """IndicatorBase class defines the base class for all indicators"""

    default_settings = {
    }

    update_type = "prices"

    async def _hidden_init_(self, id, settings, manager):
        self.id = id
        self.settings = {**self.default_settings, **settings} # gives custom settings
        self.__manager = manager
        self.ismarket = False

    def update(self, update):
        print("My update got called!", update)
        pass
