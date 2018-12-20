from bots.BotBase import BotBase

class EmaBot(BotBase):
    """The simplest of all the bots. 
    If you lose to this bot, then you should reconsider a future in the market."""

    default_settings = {
        "sleep_duration": 5, # in seconds. THIS SETTING IS REQUIRED
        "buy_limit": 3, # number of companies to buy at a time
        "stocks_per_company":3, # how many stocks per company do you want to buy at a time
        "holding_time": 5, # how many rounds to hold before you sell your stocks off
        "no_of_companies": 10, # number of companies to buy from
        "bot_tag": "unset", # special tags for searching purpose
        "k": 5
    }

    def __init__(self):
        self.settings = {}
        self.settings = {**self.default_settings, **self.settings}
        self.current_time = 0 # how many instances have occured since last buying 
        self.company_list = [] # array of [company_id, ema , latest_price]

    async def load_indicators(self):
        self.emaindicator = {}
        for i in range(1, self.settings["no_of_companies"]+1):
            self.emaindicator[i] = await self.get_indicator("EmaIndicator", i, {
                "type": "prices",
                "k": self.settings['k']
            })

    async def update(self, *args, **kwargs):
        try:
        if self.current_time == self.settings['holding_time']:
            # if you you held for long enough, sell what you bought and buy fresh
            self.current_time = 0
            if len(self.company_list) != 0 :
                for my_company in self.company_list:
                    avgprice = self.emaindicator[my_company[0]].results.get('avgprice')
                    await self.place_sell_order(my_company[0], self.settings['stocks_per_company'], avgprice, 0)
                    log_message = "EmaBot({}) sold stocks of company {} at price {}".format(self.name, str(my_company[0]) ,str(avgprice))
                    self.add_to_log(self.id, log_message)
            
            # else if it's time to sell but you haven't bought anything yet do nothing
            else:
                pass
            # after you have sold off all your previous stocks, first see which stocks are good
            self.company_list = []

            for i in range(1, self.settings['no_of_companies'] + 1):
                ema = self.emaindicator[i].results.get('ema_ratio')
                if ema:
                    latest_price = self.emaindicator[i].prices[-1]
                    self.company_list.append([i,ema,latest_price])
            
            self.company_list.sort(key=lambda x: x[1], reverse=True)
            length = self.settings['buy_limit'] if (len(self.company_list) >= self.settings['buy_limit']) else len(self.company_list)

            # buy the top selected stocks
            i = 0
            while i<length:
                # buy at market price
                await self.place_buy_order(self.company_list[i][0], self.settings['stocks_per_company'], 0, 1)
                log_message = "EmaBot({}) bought stock {}".format(self.name, str(self.company_list[i]))
                print(log_message)
                self.add_to_log(self.id, log_message)
                i = i+1

            # modify company_list to contain only the ones we bought
            self.company_list = self.company_list[:length]

            self.current_time = self.current_time + 1
        
        except Exception as e:
            log_message = "EmaBot({}) just broke. Cause: {}".format(self.name, str(e))
            print(log_message)
            self.add_to_log(self.id, log_message)
