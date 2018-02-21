"""Test script"""

import asyncio
import aiogrpc as grpc

from proto_build import DalalMessage_pb2_grpc
from proto_build.actions.Login_pb2 import LoginRequest, LoginResponse
from proto_build.actions.CreateBot_pb2 import CreateBotRequest, CreateBotResponse
from proto_build.actions.BuyStocksFromExchange_pb2 import BuyStocksFromExchangeRequest, BuyStocksFromExchangeResponse
from proto_build.actions.PlaceOrder_pb2 import PlaceOrderRequest, PlaceOrderResponse
from proto_build.actions.CancelOrder_pb2 import CancelOrderRequest, CancelOrderResponse
from proto_build.actions.GetPortfolio_pb2 import GetPortfolioRequest, GetPortfolioResponse
from proto_build.datastreams.Subscribe_pb2 import STOCK_PRICES, STOCK_EXCHANGE, MARKET_DEPTH, MARKET_EVENTS
from proto_build.datastreams.Subscribe_pb2 import SubscribeRequest

class MarketMessenger:
    """This class coordinates with the gRPC server"""

    def __init__(self, loop=None):
        """Initialize the MarketMessenger"""
        self.stocks = {}
        # self.latest_prices = {}
        # self.market_depths = {}
        # self.market_events = []
        self.bot_secret = "hellobots" # use to get bot api access on server

        #self.loop = loop

        self.__connect()
        print("Connected and got the stubs!", self.action_stub, self.stream_stub)

    def __connect(self):
        """Connect to the server"""
        cert = open('grpc-server.crt').read().encode("utf8")
        creds = grpc.ssl_channel_credentials(cert)
        channel = grpc.secure_channel(
            "139.59.47.250:443",
            creds,
            options=(('grpc.ssl_target_name_override', "localhost",),))

        self.action_stub = DalalMessage_pb2_grpc.DalalActionServiceStub(channel)
        self.stream_stub = DalalMessage_pb2_grpc.DalalStreamServiceStub(channel)

    async def start(self):
        """starts the market messenger"""

        #res = await self.create_bot("masterbot")
        #print(res)

        login_res = await self.login("1") #masterbot
        self.stocks = login_res.stock_list

        #print(login_res, self.stocks)

        return login_res
        # streams = [
        #     self.start_stock_prices_stream(),
        #     self.start_stock_exchange_stream(),
        #     self.start_market_events_stream(),
        # ]
        # # add market depth streams
        # for stock_id in self.stocks:
        #     streams.append(self.start_market_depth_stream(stock_id))

        # done, _ = await asyncio.wait(streams)

        # for future in done:
        #     print(future.result())

    def __getmd_for_bot(self, bot_userid=None):
        """Get metadata for making bot requests. Optionally get metadata so that the request
        acts as if it was made by bot_userid"""

        if bot_userid is None:
            return [("bot_secret", self.bot_secret), ("bot_user_id", "fakeid")]
        else:
            return [("bot_secret", self.bot_secret), ("bot_user_id", str(bot_userid))]

    async def create_bot(self, botname):
        """creates a bot user on the server"""

        req = CreateBotRequest(bot_user_id=botname)
        res = await self.action_stub.CreateBot(req, metadata=self.__getmd_for_bot())

        if res.status_code != CreateBotResponse.OK:
            print(res)
            raise Exception("Got non-OK code. Didn't create bot")

        return res

    async def login(self, bot_userid):
        """Performs login, gets the session_md"""

        login_req = LoginRequest(email="bot", password="bot")
        login_res = await self.action_stub.Login(login_req, metadata=self.__getmd_for_bot(bot_userid))

        if login_res.status_code == LoginResponse.InvalidCredentialsError:
            raise Exception("Got Invalid credentials error!")

        print("Login successful")

        return login_res

    ###
    ### Stream related stuff below...
    ###
    async def __get_subscription_id(self, ds_type, ds_id=""):
        """Used to get subscription id before subscribing to a stream"""
        sub_req = SubscribeRequest(data_stream_type=ds_type, data_stream_id=str(ds_id))
        sub_res = await self.stream_stub.Subscribe(sub_req, metadata=self.__getmd_for_bot())

        return sub_res.subscription_id

    async def get_stock_prices_stream(self):
        """Stock prices stream handler"""

        subsr_id = await self.__get_subscription_id(STOCK_PRICES)
        return self.stream_stub.GetStockPricesUpdates(subsr_id, metadata=self.__getmd_for_bot())
        # try:
        #     async for update in updates_iter:
        #         print("Got prices update ", update)
        # except grpc.RpcError as error:
        #     print("Got error ", error)

    async def get_market_events_stream(self):
        """Stock market events handler"""

        subsr_id = await self.__get_subscription_id(MARKET_EVENTS)
        return self.stream_stub.GetMarketEventUpdates(subsr_id, metadata=self.__getmd_for_bot())

        # try:
        #     async for update in updates_iter:
        #         print("Got event update ", update)
        # except grpc.RpcError as error:
        #     print("Got error ", error)

    async def get_stock_exchange_stream(self):
        """Stock exchange stream handler"""

        subsr_id = await self.__get_subscription_id(STOCK_EXCHANGE)
        return self.stream_stub.GetStockExchangeUpdates(subsr_id, metadata=self.__getmd_for_bot())

        # try:
        #     async for update in updates_iter:
        #         print("Got exchange update ", update)
        # except grpc.RpcError as error:
        #     print("Got error ", error)

    async def get_market_depth_stream(self, stock_id):
        """Market depth stream handler for a given stock"""

        subsr_id = await self.__get_subscription_id(MARKET_DEPTH, stock_id)
        return self.stream_stub.GetMarketDepthUpdates(subsr_id, metadata=self.__getmd_for_bot())

        # try:
        #     async for update in updates_iter:
        #         print("Got exchange update ", update)
        # except grpc.RpcError as error:
        #     print("Got error ", error)

    ###
    ### actions related stuff below...
    ###
    async def __call_action(self, method_name, req, bot_id, response_class):
        method = getattr(self.action_stub, method_name, None)
        if method is None:
            raise Exception("Method " + method_name + " not found")

        try:
            res = await method(req, metadata=self.__getmd_for_bot(bot_id))
            if res.status_code != response_class.OK:
                print("Fucked up right over here ", res)
                raise Exception("Got non OK response code: " + str(res.status_code))

        except grpc.RpcError as error:
            status_code = error.code()
            print("Got error while calling " + method_name, type(error), error.details(), status_code.name)
            raise Exception("Got unexpected error code")

        return res

    async def get_portfolio(self, bot_id):
        """get user's portfolio order"""

        req = GetPortfolioRequest()
        return await self.__call_action("GetPortfolio", req, bot_id, GetPortfolioResponse)


    async def buy_stocks_from_exchange(self, bot_id, stock_id, stock_quantity):
        """Buy stocks from Exchange"""

        req = BuyStocksFromExchangeRequest(stock_id=stock_id, stock_quantity=stock_quantity)
        return await self.__call_action("BuyStocksFromExchange", req, bot_id, BuyStocksFromExchangeResponse)

    async def place_buy_order(self, bot_id, stock_id, stock_quantity, price, order_type):
        """place Bid order"""

        req = PlaceOrderRequest(stock_id=stock_id, stock_quantity=stock_quantity, price=price, order_type=order_type)
        return await self.__call_action("PlaceOrder", req, bot_id, PlaceOrderResponse)

    async def place_sell_order(self, bot_id, stock_id, stock_quantity, price, order_type):
        """place ask order"""

        req = PlaceOrderRequest(stock_id=stock_id, stock_quantity=stock_quantity, price=price, order_type=order_type, is_ask=True)
        return await self.__call_action("PlaceOrder", req, bot_id, PlaceOrderResponse)

    async def cancel_order(self, bot_id, order_id, is_ask):
        """cancel buy/sell order"""

        req = CancelOrderRequest(order_id=order_id, is_ask=is_ask)
        return await self.__call_action("CancelOrder", req, bot_id, CancelOrderResponse)

# Master control's mother
def main():
    market_messenger = MarketMessenger()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(market_messenger.start())
    loop.close()

# Master control's grandmother
if __name__ == "__main__":
    main()
