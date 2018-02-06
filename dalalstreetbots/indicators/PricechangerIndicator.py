from indicators.IndicatorBase import IndicatorBase

class PricechangerIndicator(IndicatorBase):

    default_settings = {
        "type": "prices" # "prices" or "news". If news, it won't get prices updates
    }

    def __init__(self):
        self.price = 0

    def update(self, update):
        self.price = update