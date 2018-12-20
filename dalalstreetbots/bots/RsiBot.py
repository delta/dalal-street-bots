from bots.BotBase import BotBase

class RsiBot(BotBase):
    """The Rsi Bot.
    """

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
        "buy_limit": 3, # number of companies to buy at a time
        "stocks_per_company":3, # how many stocks per company do you want to buy at a time
        "holding_time": 3, # how many rounds to hold before you sell your stocks off
        "no_of_companies": 10, # number of companies to buy from
        "bot_tag": "unset", # special tags for searching purpose
        "k": 5,
    }

    def __init__(self):
        self.settings = {}
        self.settings = {**self.default_settings, **self.settings}
        self.current_time = 0 # how many instances have occured since last buying 
        self.company_list = [] # array of [company_id, rsi, latest_price]

    async def load_indicators(self):
        self.rsiindicator = {}
        for i in range(1, self.settings["no_of_companies"]+1):
            self.rsiindicator[i] = await self.get_indicator("RsiIndicator", i, {
                "type": "prices",
                "k": self.settings['k']
            })

    async def update(self, *args, **kwargs):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""
        try:
            if self.settings['holding_time'] == self.current_time:
                self.current_time = 0
                # if you already have bought some companies previously, sell them off and buy new ones
                if len(self.company_list) != 0 :
                    for my_company in self.company_list:
                        await self.place_sell_order(my_company[0], self.settings["stocks_per_company"], my_company[2], 0)
                        log_message = "Rsi({}) sold stocks of company {}".format(self.name, str(my_company[0]))
                        print(log_message)
                        self.add_to_log(self.id, log_message)

                self.company_list = []
                # now select companies based on rsi indicator
                for i in range(1, self.settings["no_of_companies"] + 1):
                    rsi = self.rsiindicator[i].results.get('rsi')
                    if (rsi):
                        latest_price = self.rsiindicator[i].prices[-1]
                        self.company_list.append([i,rsi, latest_price])

                self.company_list.sort(key=lambda x: x[1], reverse=True)
                length = self.settings['buy_limit'] if (len(self.company_list) >= self.settings['buy_limit']) else len(self.company_list)

                # now start buying off the stocks
                i = 0
                while i<length:
                    await self.place_buy_order(self.company_list[i][0], self.settings["stocks_per_company"], 0, 1)
                    log_message = "RsiBot({}) bought stock {}".format(self.name, str(self.company_list[i]))
                    self.add_to_log(self.id, log_message)
                    i = i+1

                self.company_list = self.company_list[:length]

            self.current_time = self.current_time + 1
        except Exception as e:
            log_message = "Rsi({}) just broke. Cause: {}".format(self.name, str(e))
            print(log_message)
            self.add_to_log(self.id, log_message)