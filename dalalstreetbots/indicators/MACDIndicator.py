from indicators.IndicatorBase import IndicatorBase

class MACDIndicator(IndicatorBase):

    default_settings = {
        "type": "prices", # "prices" or "news". If news, it won't get prices updates
        "macd_level": 4, # for signal line
        "macd_newer": 6, # the less-lagging EMA value
        "macd_lagger": 16
    }

    def __init__(self):
        self.prices = []
        self.prices_length = 0
        self.results = {"macd":"na","ema_9":"na"}

    def update(self, update):
        self.prices.append(update)
        self.prices_length = self.prices_length + 1

        if (self.prices_length < self.madc_lagger + self.settings['macd_level'] - 1):
            # Do nothing if you are here. You don't have enough data
            pass
        
        else:
            lagger_list = []
            macd_list = self.prices[-1*(self.settings['macd_lagger']+self.settings['macd_level']):]
            lagger_ema = self.k_ema(macd_list,self.settings['macd_lagger'])
            macd_list = self.prices[-1*(self.settings['macd_newer']+self.settings['macd_level']):]
            newer_ema = self.k_ema(macd_list, self.settings['macd_newer'])
            
            macd_list = []
            for i in range(self.settings['macd_level']):
                macd_list.append(newer_ema[i] - lagger_ema[i])
            self.results['macd'] = macd_list[-1] 
            macd_list = self.k_ema(macd_list, self.settings['macd_level'])
            self.results["ema_9"] = macd_list[0]
    
	def k_ema(self, series, k):
            """Returns k-EMA series from input series array
            """
    
            i = k
            ema_series = []
            ema_series.append(sum(series[0:k])/k)
    
            smoothening_factor = 2/(k+1)
    
            while i < len(series):
                next_ema = (series[i] - ema_series[-1])*smoothening_factor + ema_series[-1]
                ema_series.append(next_ema)
                i = i+1
    
            return ema_series
