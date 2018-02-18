from indicators.IndicatorBase import IndicatorBase

class StockchangerIndicator(IndicatorBase):

    default_settings = {
        "type": "prices", # "prices" or "news". If news, it won't get prices updates
    }

    def __init__(self):
        self.price = 0

    def update(self, update):
        # just store the last price and buy more and more eventually
        self.price = update