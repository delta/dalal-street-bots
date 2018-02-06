from indicators.IndicatorBase import IndicatorBase

class RSIIndicator(IndicatorBase):

    default_settings = {
        "type": "prices" # "prices" or "news". If news, it won't get prices updates
    }

    def __init__(self):
        self.prices = []
        self.prices_length = 0
        self.k = 3 
        self.rsi = 0

    def update(self, update):
        self.prices.append(update)
        self.prices_length = self.prices_length + 1

        if (self.prices_length < self.k):
            # Do nothing if you are here. You don't have enough data
            pass
        
        else:
            gain_avg = 0
            loss_avg = 0

            for i in range(self.k -1):
                diff = self.prices[self.prices_length - self.k + i + 1] - self.prices[self.prices_length - self.k + i]

                if diff >= 0:
                    gain_avg = gain_avg + diff
                else:
                    loss_avg = loss_avg + diff*-1

            rs = gain_avg/loss_avg
            self.rsi = 100 - 100/(1+rs)