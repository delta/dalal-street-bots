from indicators.IndicatorBase import IndicatorBase

class PricechangerIndicator(IndicatorBase):

    default_settings = {
        "lookup_window": 5 # sum of how many days to check with percentage_change
    }

    update_type = "prices"
    first_update = True
    previous_price = 0
    current_price = 0

    def __init__(self):
        self.prices = []

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
