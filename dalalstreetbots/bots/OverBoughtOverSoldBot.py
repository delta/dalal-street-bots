from bots.BotBase import BotBase

class OverBoughtOverSoldBot(BotBase):
    """Spread Controller Bot.
    
    Look for prices of all companies. If there's a constant decline in price, consider it oversold and 
    go long. If there's a constant increase in price, consider it over overbought and consider it overbought
    and go short.
    """

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
        "no_of_companies": 15, # number of companies to buy from. Technically should be ALL
        "bot_tag": "unset", # special tags for searching purpose
        "percentage_change": 10, # the sum percentage change before the bot starts acting
        "cut_down_factor": 2, # how much to cut down the current percentage of increase by
    }

    def __init__(self):
        self.settings = {}
        self.settings = {**self.default_settings, **self.settings}
        self.current_time = 0 # how many instances have occured since last buying 

    async def load_indicators(self):
        self.pricechangeindicator = {}
        for i in range(1, self.settings["no_of_companies"]):
            self.pricechangeindicator[i] = await self.get_indicator("PricechangerIndicator", i, {
                "type": "prices",
                "lookup_window": 5, # sum of how many days to check with percentage_change
            })

    async def update(self, *args, **kwargs):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""
        try:
            for stock_id in range(1, self.settings["no_of_companies"]):
                percentage_change = sum(self.pricechangeindicator[stock_id].prices)
                if percentage_change > self.settings['percentage_change']:
                    cut_down_percent = abs(percentage_change / self.settings['cut_down_factor'])
                    sell_price = self.pricechangeindicator[stock_id].current_price * ((100 - cut_down_percent) / 100)
                    await self.place_sell_order(stock_id, 1, int(round(sell_price)), 0)

                    log_message = "OverBoughtOverSold({}) sold stock {}".format(self.name, str(stock_id))
                    print(log_message)
                    self.add_to_log(self.id, log_message)
                elif percentage_change < self.settings['percentage_change']*-1:
                    # if percentage_change is too rapid, place buy orders at slightly higher price
                    cut_down_percent = abs(percentage_change/self.settings['cut_down_factor'])
                    buy_price = self.pricechangeindicator[stock_id].current_price * ((100 + cut_down_percent) / 100)
                    await self.place_buy_order(stock_id, 1, int(round(buy_price)), 1)
                    
                    log_message = "OverBoughtOverSold({}) bought stock {}".format(self.name, stock_id)
                    print(log_message)
                    self.add_to_log(self.id, log_message)

        except Exception as e:
            log_message = "OverBoughtOverSold({}) just broke. Cause: {}".format(self.name, str(e))
            print(log_message)
            self.add_to_log(self.id, log_message)
        