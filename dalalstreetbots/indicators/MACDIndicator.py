from indicators.IndicatorBase import IndicatorBase

class MACDIndicator(IndicatorBase):

    default_settings = {
        "type": "prices" # "prices" or "news". If news, it won't get prices updates
    }

    def __init__(self):
        self.prices = []
        self.prices_length = 0
        self.macd_lagger = 16 # 16 instead of 26
        self.macd_newer = 6   # 9 instead of 12
        self.macd_level = 4	  # 4 instead of 9

        self.results = {"macd":"na","ema_9":"na"}

    def update(self, update):
        self.prices.append(update)
        self.prices_length = self.prices_length + 1

        if (self.prices_length < self.madc_lagger + self.macd_level - 1):
            # Do nothing if you are here. You don't have enough data
            pass
        
        else:
            lagger_list = []
            macd_list = self.prices[-1*(self.macd_lagger+self.macd_level):]
            lagger_ema = self.k_ema(macd_list,self.macd_lagger)
            macd_list = self.prices[-1*(self.macd_newer+self.macd_level):]
            newer_ema = self.k_ema(macd_list, self.macd_newer)
            
            macd_list = []
            for i in range(self.macd_level):
                macd_list.append(newer_ema[i] - lagger_ema[i])
            self.results['macd'] = macd_list[-1] 
            macd_list = self.k_ema(macd_list, self.macd_level)
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
