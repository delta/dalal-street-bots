from bots.BotBase import BotBase

class RSIBot(BotBase):
    """The RSI Bot.
    """

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
    }

    def __init__(self):
        self.current_time = 0 # how many instances have occured since last buying 
        self.company_list = [] # array of [company_id, rsi, latest_price]

    async def load_indicators(self):
        self.rsiindicator = {}
        for i in range(1, self.settings["no_of_companies"]):
            self.rsiindicator[i] = await self.get_indicator("RSIIndicator", i, {})

    async def update(self, *args, **kwargs):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""

        if self.holding_time == self.current_time:

            self.current_time = 0
            # if you already have bought some companies previously, sell them off and buy new ones
            if len(self.company_list) != 0 :
                for my_company in self.company_list:
                    await self.place_sell_order(my_company[0], self.settings["stocks_per_company"], my_company[2])
                    log_message = "RSI(" + self.name + ") sold stocks of company" + str(my_company[0])
                    self.add_to_log(self.id, log_message)

            # if you don't have anything, then don't do anything
            else:
                log_message = "RSIBot(" + self.name + ") hasn't bought any companies yet"
                self.add_to_log(self.id, log_message)

            # now select companies based on rsi indicator
            for i in range(1, self.settings["no_of_companies"]):
                rsi = self.rsiindicator[i].results.get('rsi')
                if (rsi):
                    latest_price = self.rsiindicator[i].prices[-1]
                    self.company_list.append([i,rsi, latest_price])

            self.company_list.sort(key=lambda x: x[1], reverse=True)
            length = self.buy_limit if (length(self.company_list)) >= self.buy_limit) else length(self.company_list)

            # now start buying off the stocks
            i = 0
            while i<length:
                await self.buy_stocks_from_exchange(company[0], self.settings["stocks_per_company"])
                log_message = "RSIBot(" + self.name + ") bought stock " + str(self.company_list[i])
                self.add_to_log(self.id, log_message)
                i = i+1

            self.company_list = self.company_list[:length]

        else:
            # don't do anything
            log_message = "RSIBot(" + self.name + ") holding its stocks. Current time " + str(self.current_time)
            self.add_to_log(self.id, log_message)
        
        self.current_time = self.current_time + 1