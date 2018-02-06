from bots.BotBase import BotBase

class RSIBot(BotBase):
    """The RSI Bot.
    """

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
    }

    def __init__(self):
        self.holding_time = 3 # how long to hold before selling
        self.current_time = 0 # how many instances have occured since last buying 
        self.buy_limit = 3 # how many companies to buy at a time

    async def load_indicators(self):
        self.rsiindicator = {}
        for i in range(1,10):
            self.rsiindicator[i] = await self.get_indicator("RSIIndicator", i, {})

    async def update(self, *args, **kwargs):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""

        if self.holding_time == self.current_time:
            
            self.current_time = 0

            company_list = []

            for i in range(1,10):
                rsi = self.rsiindicator[i].results.get('rsi')
                if (rsi):
                    company_list.append([i,rsi])

            company_list.sort(key=lambda x: x[1], reverse=True)
            length = self.buy_limit if (length(company_list)) >= self.buy_limit) else length(company_list)

            i = 0
            while i<length:
                await self.buy_stocks_from_exchange(company[0], 3)
                print("EmaBot(" + self.name + ") update got called with ", args, kwargs)
                i = i+1
        
        self.current_time = self.current_time + 1