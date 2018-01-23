"""DumbIndicator class"""

from indicators.IndicatorBase import IndicatorBase

class DumbIndicator(IndicatorBase):
    """DumbIndicator class defines a dumb indicators"""

    default_settings = {
        "type": "prices" # "prices" or "news". If news, it won't get prices updates
    }

    def update(self, update):
        print("My update got called!", update)
        pass
