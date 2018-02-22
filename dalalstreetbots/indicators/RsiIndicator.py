from indicators.IndicatorBase import IndicatorBase

class RsiIndicator(IndicatorBase):

    default_settings = {
        "k": 3,
    }

    update_type = "prices"
    
    def __init__(self):
        self.prices = []
        self.prices_length = 0
        self.results = {}

    def update(self, update):
        self.prices.append(update)
        self.prices_length = self.prices_length + 1
        print("RSI INDICATOR ", self.settings['k'], self.prices_length)
        if (self.prices_length < self.settings['k']):
            # Do nothing if you are here. You don't have enough data
            pass
        
        else:
            gain_avg = 0
            loss_avg = 0

            for i in range(self.settings['k'] -1):
                diff = self.prices[self.prices_length - self.settings['k'] + i + 1] - self.prices[self.prices_length - self.settings['k'] + i]

                if diff >= 0:
                    gain_avg = gain_avg + diff
                else:
                    loss_avg = loss_avg + diff*-1

            rs = (gain_avg + 1)/(loss_avg + 1)
            self.results['rsi'] = 100 - 100/(1+rs)