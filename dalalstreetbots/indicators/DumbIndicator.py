"""DumbIndicator class"""

from indicators.IndicatorBase import IndicatorBase

class DumbIndicator(IndicatorBase):
    """DumbIndicator class defines a dumb indicators"""

    default_settings = {
    }

    update_type = "prices"

    def update(self, update):
        print("My update got called!", update)
        pass
