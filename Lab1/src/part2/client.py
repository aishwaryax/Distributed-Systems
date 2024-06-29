import grpc
import toy_store_pb2_grpc
import toy_store_pb2
import time
from config import SERVER_HOST, ITERS, PORT

_BUY_RESPONSE_TIME = 0
_BUY_QUERIES = 0
_QUERY_RESPONSE_TIME = 0
_QUERY_QUERIES = 0

def buy(stub, item_name):
    global _BUY_RESPONSE_TIME, _BUY_QUERIES
    start_time = time.time()
    response = None
    try:
        response = stub.Buy(toy_store_pb2.Request(ItemName=item_name)) #Buy rpc call
    except grpc.RpcError as e:
        response = e.details()
    end_time = time.time()
    _BUY_RESPONSE_TIME += end_time - start_time
    _BUY_QUERIES += 1
    return response

def query(stub, item_name):
    global _QUERY_RESPONSE_TIME, _QUERY_QUERIES
    start_time = time.time()
    response = None
    try:
        response = stub.Query(toy_store_pb2.Request(ItemName=item_name)) #Query rpc call
    except grpc.RpcError as e:
        response = e.details()
    end_time = time.time()
    _QUERY_RESPONSE_TIME += end_time - start_time
    _QUERY_QUERIES += 1
    return response

def run(num_iters):
    global _BUY_RESPONSE_TIME, _BUY_QUERIES, _QUERY_RESPONSE_TIME, _QUERY_QUERIES
    with grpc.insecure_channel(SERVER_HOST + ":" + str(PORT)) as channel: #connect to channel
        stub = toy_store_pb2_grpc.ToyStoreStub(channel) #create stub
        toys = ["Elephant", "Tux", "Dolphin", "Whale", "InValid Data"]

        for _ in range(num_iters):
            for toy in toys:
                query_response = query(stub, toy) #call query helper
                buy_response = buy(stub, toy) #call buy helper
                print("Query Response for ", toy, " - ", query_response)
                print("Buy Response for ", toy, " - ", buy_response)

if __name__ == "__main__":
    run(ITERS)
    print("Buy response time : ", _BUY_RESPONSE_TIME, " for queries : ", _BUY_QUERIES)
    print("Query response time : ", _QUERY_RESPONSE_TIME, " for queries : ", _QUERY_QUERIES)
