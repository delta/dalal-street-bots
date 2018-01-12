"""Bot class"""

class Bot(object):
    """Bot class defines the base class for all bots"""

    type_name = "BotGranddad"
    default_settings = {
        "priority": 1,        # higher has more priority. This setting is REQUIRED
        "sleep_duration": 15, # in seconds. THIS SETTING IS REQUIRED
    }

    def __init__(self, id, name, settings, manager, market_messenger):
        self.id = id
        self.name = name         # name is unique to each bot
        self.settings = settings # TODO: need to use the defaults
        self.__manager = manager # keep the manager private
        self.__market_messenger = market_messenger # keep the market messenger private

    # TODO: get_my_cash
    async def get_my_cash(self):
        """get_my_cash returns the cash owned by the bot"""
        pass

    # TODO: get_my_portfolio
    async def get_my_portfolio(self):
        """get_my_portfolio returns the portfolio of the bot"""
        pass

    async def buy_stocks_from_exchange(self, stock_id, stock_quantity):
        """Buy stocks from Exchange"""
        return await self.__market_messenger.buy_stocks_from_exchange(
            self.id, stock_id, stock_quantity
        )

    async def place_buy_order(self, stock_id, stock_quantity, price):
        """place Bid order"""
        return await self.__market_messenger.place_buy_order(
            self.id, stock_id, stock_quantity, price
        )

    async def place_sell_order(self, stock_id, stock_quantity, price):
        """place ask order"""
        return await self.__market_messenger.place_sell_order(
            self.id, stock_id, stock_quantity, price
        )

    async def cancel_order(self, order_id, is_ask):
        """cancel buy/sell order"""
        return await self.__market_messenger.cancel_order(
            self.id, order_id, is_ask
        )
