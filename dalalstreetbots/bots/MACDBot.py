from bots.BotBase import BotBase

class MACDBot(BotBase):
    """The MACD Bot
    """

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
    }

    def __init__(self):
        self.holding_time = 3 # how long to hold before selling
        self.current_time = 0 # how many instances have occured since last buying 
        self.buy_limit = 3 # how many companies to buy at a time
        self.macd_old = 15
        self.macd_new = 6

    async def load_indicators(self):
        self.rsiindicator = {}
        for i in range(1,10):
            self.rsiindicator[i] = await self.get_indicator("MACDIndicator", i, {})

    async def update(self, *args, **kwargs):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""

        self.current_time = 0

            company_list = []

            for i in range(1,10):
                macd = self.emaindicator[i].results.get('macd')
                ema_9 = self.emaindicator[i].results.get('ema_9')
                if (ema_9 != "na" && macd !="na"):
                    company_list.append([i,macd - ema_9])
            
            company_list.sort(key=lambda x: x[1], reverse=True)
            length = self.buy_limit if (len(company_list)) >= self.buy_limit) else len(company_list)

            i = 0
            while i<length:
                await self.buy_stocks_from_exchange(company_list[i][0], 3)
                print("MACDBot(" + self.name + ") update got called with ", args, kwargs)
                i = i+1

        self.current_time = self.current_time + 1