from indicators.IndicatorBase import IndicatorBase

class PricechangerIndicator(IndicatorBase):

    default_settings = {
    }

    update_type = "prices"

    def __init__(self):
        self.price = 0

    def update(self, update):
        self.price = update