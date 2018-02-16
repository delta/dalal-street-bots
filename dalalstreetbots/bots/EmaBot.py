from bots.BotBase import BotBase

class EmaBot(BotBase):
    """The simplest of all the bots. 
    If you lose to this bot, then you should reconsider a future in the market."""

    specific_settings = {
        "k": 3 # value of k in k-EMA
    }

    def __init__(self):
        self.settings = {}
        self.settings = {**self.specific_settings, **self.settings}
        self.current_time = 0 # how many instances have occured since last buying 
        self.company_list = [] # array of [company_id, ema , latest_price]

    async def load_indicators(self):
        self.emaindicator = {}
        for i in range(1, self.settings["no_of_companies"]):
            self.emaindicator[i] = await self.get_indicator("EmaIndicator", i, {
                "type": "prices",
                "k": self.settings['k']
            })

    async def update(self, *args, **kwargs):

        if self.current_time == self.settings['holding_time']:
            # if you you held for long enough, sell what you bought and buy fresh
            self.current_time = 0
            if len(self.company_list) != 0 :
                for my_company in self.company_list:
                    await self.place_sell_order(my_company[0], self.settings['stocks_per_company'], my_company[2])
                    log_message = "EmaBot(" + self.name + ") sold stocks of company" + str(my_company[0])
                    self.add_to_log(self.id, log_message)
            
            # else if it's time to sell but you haven't bought anything yet do nothing
            else:
                log_message = "EmaBot(" + self.name + ") hasn't bought any companies yet"
                self.add_to_log(self.id, log_message)

            # after you have sold off all your previous stocks, first see which stocks are good
            self.company_list = []

            for i in range(1, self.settings["no_of_companies"]):
                ema = self.emaindicator[i].results.get('ema_ratio')
                latest_price = self.emaindicator[i].prices[-1]
                if (ema):
                    self.company_list.append([i,ema,latest_price])
            
            self.company_list.sort(key=lambda x: x[1], reverse=True)
            length = self.settings['buy_limit'] if (len(self.company_list) >= self.settings['buy_limit']) else len(self.company_list)

            # buy the top selected stocks
            i = 0
            while i<length:
                # buy at market price
                await self.place_buy_order(self.company_list[i][0], self.settings['stocks_per_company'], 0, 1)
                log_message = "EmaBot(" + self.name + ") bought stock " + str(self.company_list[i])
                self.add_to_log(self.id, log_message)
                i = i+1

            # modify company_list to contain only the ones we bought
            self.company_list = self.company_list[:length]

        else:
            # don't do anything
            log_message = "EmaBot(" + self.name + ") holding its stocks. Current time " + str(self.current_time)
            self.add_to_log(self.id, log_message)

        self.current_time = self.current_time + 1