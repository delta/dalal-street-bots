"""Test script"""

import asyncio
import aiogrpc as grpc

from proto_build import DalalMessage_pb2_grpc
from proto_build.actions.Login_pb2 import LoginRequest, LoginResponse
from proto_build.actions.BuyStocksFromExchange_pb2 import BuyStocksFromExchangeRequest, BuyStocksFromExchangeResponse
from proto_build.datastreams.Subscribe_pb2 import NOTIFICATIONS, STOCK_PRICES, SubscriptionId, SubscribeRequest, SubscribeResponse

actionStub = None
streamStub = None

# Notifications stream handler
async def notificationsStream(session_md):
    subReq = SubscribeRequest(data_stream_type=NOTIFICATIONS, data_stream_id="")
    subRes = await streamStub.Subscribe(subReq, metadata=session_md)

    subsrId = subRes.subscription_id
    updateStrItr = streamStub.GetNotificationUpdates(subsrId, metadata=session_md)
    try:
        async for update in updateStrItr:
            print("Got notifications update ", update)
    except grpc.RpcError as e:
        print("Got error ", e)

# Stock prices stream handler
async def stockPricesStream(session_md):
    subReq = SubscribeRequest(data_stream_type=STOCK_PRICES, data_stream_id="1")
    subRes = await streamStub.Subscribe(subReq, metadata=session_md)

    subsrId = subRes.subscription_id
    updateStrItr = streamStub.GetStockPricesUpdates(subsrId, metadata=session_md)
    try:
        async for update in updateStrItr:
            print("Got prices update ", update)
    except grpc.RpcError as e:
        print("Got error ", e)

# Buy stocks from Exchange stream handler
async def BuyStocksFromExchange(session_md):
    try:
        buyReq = BuyStocksFromExchangeRequest(stock_id=1, stock_quantity=10)
        buyRes = await actionStub.BuyStocksFromExchange(buyReq, metadata=session_md)
        print("Got reponse ", buyRes)
    except grpc.RpcError as e:
        status_code = e.code()
        if status_code.name != "UNAUTHENTICATED":
            raise Exception("Got unexpected error code " + status_code)
        print("Got error ", type(e), e.details(), status_code.name)

# Login
async def login():
    #loginReq = LoginRequest(email="test@test.com", password="test")
    loginReq = LoginRequest(email="106114062@nitt.edu", password="mahpasswordmahlife123")
    loginRes = await actionStub.Login(loginReq)
    print("Got response ", loginRes)
    print("Hello ", loginRes.status_code == LoginResponse.InvalidCredentialsError)

    print("\n")

    session_md = [("sessionid", loginRes.session_id)]
    print("Using session ", loginRes.session_id)
    return session_md

# Master controller
async def run():
    session_md = await login()
    # streamFutures = map(lambda fn: fn(session_md), [notificationsStream, stockPricesStream])
    done, _ = await asyncio.wait([
        notificationsStream(session_md),
        stockPricesStream(session_md),
        BuyStocksFromExchange(session_md)
    ])

    for future in done:
        print(future.result())

# Connect to the server
def connect():
    global actionStub, streamStub

    cert = open('grpc-server.crt').read().encode("utf8")
    creds = grpc.ssl_channel_credentials(cert)
    channel = grpc.secure_channel("localhost:8000", creds)

    actionStub = DalalMessage_pb2_grpc.DalalActionServiceStub(channel)
    streamStub = DalalMessage_pb2_grpc.DalalStreamServiceStub(channel)

# Master control's mother
def main():
    connect()
    print("Connected and got the stubs!", actionStub, streamStub)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()

# Master control's grandmother
if __name__ == "__main__":
    main()
