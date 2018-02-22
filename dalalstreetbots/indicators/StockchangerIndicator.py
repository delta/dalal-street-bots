from indicators.IndicatorBase import IndicatorBase

class StockchangerIndicator(IndicatorBase):

    default_settings = {
    }

    update_type = "prices"

    def __init__(self):
        self.price = 0

    def update(self, update):
        # just store the last price and buy more and more eventually
        print("Got price update ",update)
        self.price = update