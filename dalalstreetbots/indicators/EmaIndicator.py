from indicators.IndicatorBase import IndicatorBase

class EmaIndicator(IndicatorBase):

    default_settings = {
        "type": "prices", # "prices" or "news". If news, it won't get prices updates
        "k": 3  # value of k in k-EMA
    }

    def __init__(self):
        self.prices = []
        self.ema_history = []
        self.prices_length = 0
        self.results = {}

    def update(self, update):
        self.prices.append(update)
        self.prices_length = self.prices_length + 1

        if (self.prices_length < self.settings['k']):
            # Do nothing if you are here. You don't have enough data
            pass
        
        elif (self.prices_length == self.settings['k']):
            # The first time, it's just the average
            self.ema_history.append(sum(self.prices[:])/self.settings['k'])
            self.results['ema_ratio'] = (self.ema_history[-1])/update

        else:
            # Next time onwards, it's using the formula for ema
            next_ema = (update - self.ema_history[-1])*2/(self.settings['k']+1) + self.ema_history[-1]
            self.ema_history.append(next_ema)
            self.results['ema_ratio'] = (next_ema)/update