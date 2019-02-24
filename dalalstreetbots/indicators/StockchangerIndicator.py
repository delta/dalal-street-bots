from indicators.IndicatorBase import IndicatorBase

class StockchangerIndicator(IndicatorBase):

    default_settings = {
        "lookup_window": 5 # sum of how many days to check with percentage_change
    }

    update_type = "prices"

    def __init__(self):
        self.price = 0
        self.prices = []

    def update(self, update):
        # just store the last price and buy more and more eventually
        self.price = update
        self.prices.append(update)
        if len(self.prices) > self.settings['lookup_window']:
            self.prices.pop(0)
