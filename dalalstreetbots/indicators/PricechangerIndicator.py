from indicators.IndicatorBase import IndicatorBase

class PricechangerIndicator(IndicatorBase):

    default_settings = {
        "lookup_window": 5 # sum of how many days to check with percentage_change
    }

    def __init__(self):
        self.prices = []
        self.update_type = "prices"
        self.first_update = True
        self.previous_price = 0
        self.current_price = 0

    def update(self, update):
        if self.first_update:
            self.first_update = False
            self.previous_price = self.current_price = update
        else:
            self.current_price = update
            percentage = (self.current_price - self.previous_price)/self.previous_price*100.0
            self.prices.append(percentage)
            if len(self.prices) == self.default_settings['lookup_window']:
                self.prices.pop(0)
            self.previous_price = update
