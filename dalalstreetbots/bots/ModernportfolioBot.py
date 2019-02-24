from bots.BotBase import BotBase
import random
from math import sqrt
import traceback

class ModernportfolioBot(BotBase):
    """Modernportfolio acts as the market maker for Dalalstreet

    Modernportfolio bot picks last n companies and buys them. The bot then
    holds the companies for a given amount of time and sells the whole thing together
    when it's making a net profit.
    """

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
        "no_of_companies": 15, # number of companies to buy from. Technically should be ALL
        "bot_tag": "unset", # special tags for searching purpose
        "n": 6, # number of companies for the buy-and-hold strategy
        'lookup_window': 5,  # number of entries to look for in indicator
        'trade_wait_duration': 5,  # amount to wait before you can sell whatever you bought
    }

    def __init__(self):
        self.settings = {}
        self.settings = {**self.default_settings, **self.settings}
        self.last_long = 0
        self.last_short = 0
    
    async def load_indicators(self):
        self.pricechangerindicator = {}
        for i in range(1, self.settings["no_of_companies"]+1):
            self.pricechangerindicator[i] = await self.get_indicator("PricechangerIndicator", i, {
                "lookup_window": self.settings['lookup_window'],
            })
    
    def covar(self, x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        return sum((a - mean_x) * (b - mean_y) for (a,b) in zip(x,y)) / len(x)
    
    def variance(self, x):
        mean_x = sum(x) / len(x)
        return sum((a - mean_x) *(a - mean_x)  for a in x) / len(x)
    
    def corr(self, x, y):
        return self.covar(x, y) / (sqrt(self.variance(x) * self.variance(y)) + 1)
    
    def generate_market_data(self, market_increase):
        market_increase = [0 for i in range(1, self.settings['lookup_window']+1)]
        for i in range(1, self.settings['no_of_companies']+1):
            percentage_change = self.pricechangerindicator[i].prices
            for j in range(len(percentage_change)):
                market_increase[j] += percentage_change[j]/self.settings['no_of_companies']
        return market_increase
    
    async def update(self, *args, **kwargs):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""
        try:
            # Once we have enough data on each company, we can start bot
            if all([len(x.prices) == self.settings['lookup_window'] for x in self.pricechangerindicator.values()]):
                if self.last_short == 0 and self.last_long == 0:
                    market_increase = []
                    # generate Market Index. I'm just taking average of everything and assuming that works as the index.
                    # If this code does poorly, blame this assumption
                    market_increase = self.generate_market_data(market_increase)
                    results = []
                    # Generate results based on market index
                    for stock_id in range(1, self.settings['no_of_companies']+1):
                        most_recent_price_changes = self.pricechangerindicator[stock_id].prices
                        most_recent_price = self.pricechangerindicator[stock_id].current_price

                        corr = self.corr(market_increase, most_recent_price_changes)
                        beta = self.covar(market_increase, most_recent_price_changes) / self.variance(market_increase)
                        results.append((stock_id, corr, beta, most_recent_price))
                    # Split data to positive and negative correlation. Now pick the least risky stocks
                    # The objective here is to buy less risky stocks for pos_corr and short sell
                    pos_corr = []
                    neg_corr = []
                    for obj in results:
                        if obj[1] < 0:
                            neg_corr.append(obj)
                        else:
                            pos_corr.append(obj)
                    neg_corr.sort(key=lambda x: x[2])
                    pos_corr.sort(key=lambda x: x[2])
                    neg_corr = neg_corr[:3]
                    pos_corr = pos_corr[:3]
                    # If market has a negative trend, short pos_corr and long neg_corr
                    # If market has a positive trean, long pos_corr and short neg_corr
                    if sum(market_increase) > 0:
                        short_stocks, long_stocks = neg_corr, pos_corr
                    else:
                        short_stocks, long_stocks  = pos_corr, neg_corr
                    # buy stocks
                    max_worth = max([obj[3] for obj in pos_corr + neg_corr])                    
                    for obj in short_stocks:
                        self.last_short = self.settings['trade_wait_duration']
                        e = random.randint(1, 3)
                        await self.place_sell_order(obj[0], int(round(max_worth/obj[3])), int(obj[3] - e), 0)
                    for obj in long_stocks:
                        self.last_long = self.settings['trade_wait_duration']
                        e = random.randint(1, 3)
                        await self.place_buy_order(obj[0], int(round(max_worth/obj[3])), int(obj[3] + e), 0)
                else:
                    self.last_long = max(self.last_long - 1, 0)
                    self.last_short = max(self.last_short - 1, 0)
        except Exception as e:
            log_message = "MordernportfolioBot({}) just broke. Cause: {}".format(self.name, str(e))
            print(log_message)
            error_traceback = ''.join(traceback.format_tb(e.__traceback__))
            error_message = "Got Error: {} @@@ {}".format(str(e), error_traceback)
            self.write_to_logs(self.id, error_message)


                


                
                
                    


                    
            