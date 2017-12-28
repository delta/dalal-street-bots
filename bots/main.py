"""Test script"""

import grpc

from proto_build import DalalMessage_pb2_grpc
from proto_build.actions.Login_pb2 import LoginRequest, LoginResponse
from proto_build.actions.BuyStocksFromExchange_pb2 import BuyStocksFromExchangeRequest, BuyStocksFromExchangeResponse

actionStub = None
streamStub = None

def run():
    loginReq = LoginRequest(email="test@test.com", password="test")
    loginRes = actionStub.Login(loginReq)
    print("Got response ", loginRes)
    print("Hello ", loginRes.status_code == LoginResponse.InvalidCredentialsError)

    print("\n")

    try:
        buyReq = BuyStocksFromExchangeRequest(stock_id=1, stock_quantity=10)
        buyRes = actionStub.BuyStocksFromExchange(buyReq)
        print("Got reponse ", buyRes)
    except grpc.RpcError as e:
        status_code = e.code()
        if status_code.name != "UNAUTHENTICATED":
            raise Exception("Got unexpected error code " + status_code)
        print("Got error ", type(e), e.details(), status_code.name)

if __name__ == "__main__":
    cert = open('grpc-server.crt').read().encode("utf8")
    creds = grpc.ssl_channel_credentials(cert)
    channel = grpc.secure_channel("localhost:8000", creds)

    actionStub = DalalMessage_pb2_grpc.DalalActionServiceStub(channel)
    streamStub = DalalMessage_pb2_grpc.DalalStreamServiceStub(channel)

    print("Conncted and got the stubs!", actionStub, streamStub)
    run()