from bots.BotBase import BotBase

class MacdBot(BotBase):
    """The MACD Bot
    """

    default_settings = {
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
        "buy_limit": 3, # number of companies to buy at a time
        "stocks_per_company":3, # how many stocks per company do you want to buy at a time
        "holding_time": 3, # how many rounds to hold before you sell your stocks off
        "no_of_companies": 10, # number of companies to buy from
        "bot_tag": "unset", # special tags for searching purpose
        "macd_level": 3, # for signal line
        "macd_newer": 5, # the less-lagging EMA value
        "macd_lagger": 7, # the more - lagging EMA value
    }

    def __init__(self):
        self.settings = {}
        self.settings = {**self.default_settings, **self.settings}
        self.current_time = 0 # how many instances have occured since last buying 
        self.company_list = [] # array of [id, macd, latest_price]

    async def load_indicators(self):
        self.macdindicator = {}
        for i in range(1, self.settings["no_of_companies"]):
            self.macdindicator[i] = await self.get_indicator("MacdIndicator", i, {
                "type": "prices",
                "macd_level" : self.settings['macd_level'],
                "macd_newer" : self.settings['macd_newer'],
                "macd_lagger": self.settings["macd_lagger"]
            })

    async def update(self, *args, **kwargs):
        """update method MUST BE OVERRIDDEN by *all* bots inheriting BotBase"""

        if self.current_time == self.settings['holding_time']:
            # if holding time is over, sell everything and buy new stocks
            self.current_time = 0

            # if you have bought some stocks already, sell them
            if len(self.company_list) != 0 :
                for my_company in self.company_list:
                    await self.place_sell_order(my_company[0], self.settings["stocks_per_company"], my_company[2])
                    log_message = "MACDBot(" + self.name + ") sold stocks of company" + str(my_company[0])
                    self.add_to_log(self.id, log_message)
            # else, do nothing. Just log it
            else:
                log_message = "MACDBot(" + self.name + ") hasn't bought any companies yet"
                print(log_message)
                self.add_to_log(self.id, log_message)

            # once you are done clearing your old stocks, buy new ones
            self.company_list = []

            # select new companies
            for i in range(1, self.settings["no_of_companies"]):
                macd = self.macdindicator[i].results.get('macd')
                ema_9 = self.macdindicator[i].results.get('ema_9')
                if (ema_9 != "na" and macd !="na"):
                    latest_price = self.macdindicator[i].prices[-1]
                    self.company_list.append([i,macd - ema_9, latest_price])

            self.company_list.sort(key=lambda x: x[1], reverse=True)
            length = self.settings['buy_limit'] if (len(self.company_list) >= self.settings['buy_limit']) else len(self.company_list)

            # buy new companies
            i = 0
            while i<length:
                await self.buy_stocks_from_exchange(self.company_list[i][0], self.settings["stocks_per_company"])
                log_message = "MACDBot(" + self.name + ") bought stock " + str(self.company_list[i])
                print(log_message)
                self.add_to_log(self.id, log_message)
                i = i+1

            self.company_list = self.company_list[:length]

        else:
            # don't do anything
            log_message = "MACDBot(" + self.name + ") holding its stocks. Current time " + str(self.current_time)
            print(log_message)
            self.add_to_log(self.id, log_message)

        self.current_time = self.current_time + 1